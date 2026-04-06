from ultralytics import YOLO
import cv2
import os

# Load model (first time downloads automatically)
model = YOLO("yolov8n.pt")  

def detect_and_crop(image_path, output_dir="crops"):
    os.makedirs(output_dir, exist_ok=True)

    results = model(image_path)
    image = cv2.imread(image_path)

    crops = []
    count = 0

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            # Filter only animals (important!)
            if label not in ["cat", "dog", "bird", "horse", "cow", "sheep"]:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            crop = image[y1:y2, x1:x2]
            crop_path = os.path.join(output_dir, f"crop_{count}.jpg")
            cv2.imwrite(crop_path, crop)

            crops.append({
                "label": label,
                "path": crop_path
            })

            count += 1

    return crops