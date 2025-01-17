from ultralytics import YOLO
import os
import shutil

# Load YOLO model
model = YOLO("yolov8l.pt")  # Load the YOLOv8 model

# Function to detect objects in an image
def detect_objects(image_path):
    results = model(image_path)  # Run inference on the image
    detections = results[0].boxes  # Extract bounding boxes from the first image's results
    detected_labels = []
    
    for box in detections:
        label = box.cls.item()  # Extract the class index as a number
        detected_labels.append(model.names[int(label)])  # Map index to class name using model.names

    return detected_labels

# Function to organize images based on detected objects
def organize_by_objects(directory):
    image_paths = [os.path.join(directory, f) for f in os.listdir(directory) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    
    for path in image_paths:
        try:
            objects = detect_objects(path)  # Detect objects in the image
            if objects:
                for obj in objects:
                    obj_dir = os.path.join(directory, obj)  # Ensure the object name is used as a string
                    os.makedirs(obj_dir, exist_ok=True)
                    shutil.move(path, os.path.join(obj_dir, os.path.basename(path)))
                print(f"Processed {path}, detected: {', '.join(objects)}")
            else:
                print(f"No objects detected in {path}.")
        except Exception as e:
            print(f"Error processing {path}: {e}")

# Main execution
#if __name__ == "__main__":
#    directory = "C:/Users/megha/Desktop/Download - Copy/picture"  # Update to your directory path
#    organize_by_objects(directory)
