import cv2
from image_detection import detect_nudity, is_nsfw

def process_video(video_path, threshold=0.01):
    cap = cv2.VideoCapture(video_path)
    frame_number = 0
    results = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_path = f"frame_{frame_number}.jpg"
        cv2.imwrite(frame_path, frame)
        nsfw_score = detect_nudity(frame_path)
        
        if is_nsfw(nsfw_score, threshold):
            # Draw a red bounding box around the entire frame
            height, width, _ = frame.shape
            cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), 10)
        
        results.append((frame_number, nsfw_score, is_nsfw(nsfw_score, threshold)))
        frame_number += 1

    cap.release()
    return results
