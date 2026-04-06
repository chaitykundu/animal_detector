import cv2
import os

def extract_frames(video_path, output_dir="frames", interval=30):
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if count % interval == 0:
            path = os.path.join(output_dir, f"frame_{count}.jpg")
            cv2.imwrite(path, frame)
            frames.append(path)

        count += 1

    cap.release()
    return frames