import cv2
import os

def extract_unique_frames(video_path, output_dir, frame_interval=15):
    """
    Slices a video into individual images at a set interval.
    frame_interval=15 means it saves roughly 2 images for every second of a 30fps video.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Couldn't open video file {video_path}")
        return

    frame_count = 0
    saved_count = 0

    print("Starting frame extraction...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # End of video reached

        # Process every Nth frame to avoid saving thousands of identical duplicates
        if frame_count % frame_interval == 0:
            # Resize down slightly to save storage and optimize cloud uploading later
            resized_frame = cv2.resize(frame, (640, 480))
            
            # Save frame locally as a sequential JPEG
            filename = f"box_frame_{saved_count:04d}.jpg"
            file_path = os.path.join(output_dir, filename)
            cv2.imwrite(file_path, resized_frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"Extraction complete! Saved {saved_count} unique images to '{output_dir}'.")

if __name__ == "__main__":
    # Ensure this matches your exact filename inside data/raw_videos/
    VIDEO_FILE = "data/raw_videos/box_video.mp4" 
    OUTPUT_FOLDER = "data/extracted_frames"
    
    extract_unique_frames(VIDEO_FILE, OUTPUT_FOLDER, frame_interval = 15)