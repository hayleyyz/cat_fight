import cv2
import base64
import os
from ultralytics import YOLO
from PIL import Image
import io

model = YOLO('yolov8n.pt')

def extract_cat_portraits(video_path: str) -> list[str]:
    """
    Extracts individual portraits of cats from a video file using YOLO object detection.

    Args:
        video_path: The local path to the video file.

    Returns:
        A list of base64-encoded strings, each being a JPEG image of a single detected cat.
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Error opening video file: {video_path}")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps if fps > 0 else 0
        num_frames_to_extract = 5
        
        frames = []
        for i in range(num_frames_to_extract):
            frame_index = int(total_frames * (i + 1) / (num_frames_to_extract + 1))
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            success, frame = cap.read()
            if success:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame_rgb)

        if not frames:
            raise ValueError("Could not extract any frames from the video.")

        best_frame = None
        max_cats_detected = 0
        best_frame_results = None

        print("Analyzing frames to find the one with the most cats...")
        for frame in frames:
            results = model(frame, verbose=False)
            cats_in_frame = 0
            for r in results:
                for box in r.boxes:
                    if model.names[int(box.cls)] == 'cat':
                        cats_in_frame += 1
            
            if cats_in_frame > max_cats_detected:
                max_cats_detected = cats_in_frame
                best_frame = frame
                best_frame_results = results

        if max_cats_detected == 0:
            print("No cats were detected in any of the extracted frames.")
            return []

        print(f"Found a frame with {max_cats_detected} cat(s). Cropping portraits...")

        cat_portraits_base64 = []
        pil_image = Image.fromarray(best_frame)

        for r in best_frame_results:
            for box in r.boxes:
                if model.names[int(box.cls)] == 'cat':
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    cat_portrait_pil = pil_image.crop((x1, y1, x2, y2))
                    
                    buffered = io.BytesIO()
                    cat_portrait_pil.save(buffered, format="JPEG")
                    base64_portrait = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    cat_portraits_base64.append(base64_portrait)

        return cat_portraits_base64

    finally:
        if 'cap' in locals() and cap.isOpened():
            cap.release()
