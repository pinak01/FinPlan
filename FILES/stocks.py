from ultralyticsplus import YOLO
import cv2
import matplotlib.pyplot as plt

# Load model
model = YOLO('foduucom/stockmarket-pattern-detection-yolov8')

# Set model parameters
model.overrides['conf'] = 0.25  # NMS confidence threshold
model.overrides['iou'] = 0.45  # NMS IoU threshold
model.overrides['agnostic_nms'] = False  # NMS class-agnostic
model.overrides['max_det'] = 1000  # Maximum number of detections per image

# Initialize video capture
video_path = "stocks.mp4"
cap = cv2.VideoCapture(video_path)

# Function to display frame using matplotlib
def display_frame(frame):
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.axis('off')  # Hide the axis
    plt.show()

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Check for detections
        if results[0].boxes:
            # Visualize the results on the frame
            annotated_frame = results[0].plot()
            
            # Display the annotated frame using matplotlib
            display_frame(annotated_frame)

    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object
cap.release()
