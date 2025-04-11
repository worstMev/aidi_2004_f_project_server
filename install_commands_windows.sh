#!/bin/bash
echo "INFO : create virtual environment python named venv" &&
python -m venv myvenv &&
echo "INFO : pip install fastapi and  uvicorn and numpy" &&
./myvenv/Scripts/pip install "fastapi[standard]" uvicorn &&
echo "INFO : pip install wosrtMev/python-socketio" &&
./myvenv/Scripts/pip install -e git+https://github.com/worstMev/python-engineio-wosrtMev.git#egg=engineio_worstMev &&
./myvenv/Scripts/pip install -e git+https://github.com/worstMev/python-socketio-worstMev.git#egg=python_socket_io_worstMev &&
echo "INFO: pip install cv2 deepface and tf-keras and pytorch" &&
./myvenv/Scripts/pip install deepface &&
./myvenv/Scripts/pip install tf-keras &&
./myvenv/Scripts/pip install torch 
