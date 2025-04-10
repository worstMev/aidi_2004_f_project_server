from fastapi import FastAPI,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import socketio
import numpy as np
import cv2
import base64
from deepface import DeepFace

origins_all = '*'
app = FastAPI();

#configure socket io server
sio = socketio.AsyncServer(async_mode = 'asgi',
                           #cors_allowed_origins = origins_all, custom socket io is only cors
                           allowEIO3 = True,
                           )
sio_app = socketio.ASGIApp(sio, socketio_path='/ws/socket.io')
app.mount('/ws', sio_app)

#configure fastapi
app.add_middleware(
        CORSMiddleware,
        allow_origins = origins_all,
        allow_credentials = True,
        allow_methods=['*'],
        allow_headers=['*']
        )
# test api
@app.get('/')
def root() :
    return { 'message' : 'Hello world' }


# handle socket-io events ==========================================================
@sio.event
async def connect(sid, *args, **kwargs):
    print(f'{sid} connected')
    await sio.emit( 'hello', { 'data' : 'hello world' }, to=sid);
    return

@sio.on('head_count_stream')
async def handle_head_count_stream(sid, *args, **kwargs) :
    print('handle_head_count_stream')
    blob = args[0]['blob']
    nparr = np.frombuffer(blob, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    await sio.emit('received_pic', to =sid)
    res = count_head(frame)

    processed_frame = res.get('frame')
    number = res.get('nb');

    ret, buffer = cv2.imencode('.jpg', processed_frame)
    processed_base64 = base64.b64encode(buffer).decode('utf-8')
    data_url = "data:image/jpeg;base64," + processed_base64
    # Return the processed image in the JSON response.
    feedback = {"processed" : True, "image": data_url}

    await sio.emit('feedback' , { 'feedback' : feedback } , to = sid)
    await sio.emit('head_count', {'number' : number} , to = sid)


def count_head(frame) :
    print('count_head')
    try:
        faces = DeepFace.extract_faces(img_path=frame,
                                        detector_backend="retinaface",
                                        enforce_detection=False,
                                        anti_spoofing=False,)
    except Exception as e:
        print("Error during face extraction:", e)
        return frame


    nb = 1;
    for face in faces :
        facial_area = face.get("facial_area")
        x = facial_area["x"]
        y = facial_area["y"]
        w = facial_area["w"]
        h = facial_area["h"]
        label = f'person #{nb}';
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)
        cv2.putText(frame, label, (x, y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return { 'frame' : frame, 'nb' : len(faces) }
