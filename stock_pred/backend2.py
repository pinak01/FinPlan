from flask import Flask, render_template
from flask_socketio import SocketIO
from ultralyticsplus import YOLO
import cv2
import numpy as np
import base64
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Ensure the template folder is correctly set
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app.template_folder = template_dir

# Load model
model = YOLO('foduucom/stockmarket-pattern-detection-yolov8')

# Set model parameters
model.overrides['conf'] = 0.25  # NMS confidence threshold
model.overrides['iou'] = 0.45  # NMS IoU threshold
model.overrides['agnostic_nms'] = False  # NMS class-agnostic
model.overrides['max_det'] = 1000  # Maximum number of detections per image

def process_frame(frame_data):
    # Decode base64 image
    img_data = base64.b64decode(frame_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Run YOLOv8 inference on the frame
    results = model(frame)

    # Visualize the results on the frame if there are detections
    annotated_frame = results[0].plot()
    
    # Encode frame back to base64
    _, buffer = cv2.imencode('.jpg', annotated_frame)
    frame_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return frame_base64, len(results[0].boxes) > 0

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('screen_data')
def handle_screen_data(data):
    processed_frame, has_detections = process_frame(data)
    socketio.emit('processed_frame', {'image': processed_frame, 'has_detections': has_detections})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True,port=5002)