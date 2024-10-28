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

# Keep track of the previous detection
last_detection = None

def process_frame(frame_data):
    # Decode base64 image
    img_data = base64.b64decode(frame_data.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Run YOLOv8 inference on the frame
    results = model(frame)
    
    # If there are detections, process them
    if len(results[0].boxes) > 0:
        detection_label = results[0].names[0]  # Get the label of the first detected object
        annotated_frame = results[0].plot()
        
        # Encode frame back to base64
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return detection_label, frame_base64, True
    else:
        return None, None, False

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('screen_data')
def handle_screen_data(data):
    global last_detection
    detection_label, processed_frame, has_detections = process_frame(data)
    
    # Process and filter detection results
    if has_detections:
        # Emit the detection if it's different from the last one or if it's after "no detection"
        if detection_label != last_detection:
            socketio.emit('processed_frame', {'image': processed_frame, 'has_detections': has_detections, 'detection_label': detection_label})
            last_detection = detection_label
    else:
        # Reset the last detection to ensure the next valid detection is emitted
        last_detection = None

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True,port=5002)


