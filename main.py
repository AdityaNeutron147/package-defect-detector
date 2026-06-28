import os
import time
import cv2
from ultralytics import YOLO

# Options: 'webcam', 'video', or 'image'
INPUT_MODE = 'image' 
INPUT_PATH = 'test_box_03.png' 
MODEL_PATH = "models/package_defect_v2.pt"
CONF_THRESHOLD = 0.25
SAVE_DIR = "detected_defects"

os.makedirs(SAVE_DIR, exist_ok=True)

model = YOLO(MODEL_PATH)

if INPUT_MODE == 'webcam':
    cap = cv2.VideoCapture(0)
elif INPUT_MODE == 'video':
    cap = cv2.VideoCapture(INPUT_PATH)
elif INPUT_MODE == 'image':
    cap = None
else:
    raise ValueError("Invalid INPUT_MODE. Choose 'webcam', 'video', or 'image'.")

stats = {
    "total_defects_detected": 0,
    "dent": 0,
    "dirt": 0,
    "hole": 0
}

prev_time = 0
fps = 0

print(f"Starting defect detector in [{INPUT_MODE}] mode...")

while True:
    if INPUT_MODE == 'image':
        frame = cv2.imread(INPUT_PATH)
        if frame is None:
            print(f"Error: Could not read image at {INPUT_PATH}")
            break
    else:
        ret, frame = cap.read()
        if not ret:
            print("Finished processing video or failed to grab frame.")
            break

    results = model.predict(source=frame, conf=CONF_THRESHOLD, verbose=False)
    
    defect_in_frame = False
    
    for result in results:
        annotated_frame = result.plot()
        
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id].lower()
            
            if class_name in stats:
                stats[class_name] += 1
                defect_in_frame = True
                stats["total_defects_detected"] += 1

    if 'annotated_frame' not in locals():
        annotated_frame = frame.copy()

    if defect_in_frame:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot_name = f"{SAVE_DIR}/defect_{timestamp}_{time.time_ns()}.png"
        cv2.imwrite(screenshot_name, frame)

    if INPUT_MODE != 'image':
        current_time = time.time()
        if current_time - prev_time > 0:
            fps = 1 / (current_time - prev_time)
        prev_time = current_time

    cv2.rectangle(annotated_frame, (5, 5), (280, 150), (0, 0, 0), -1)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 255, 255)
    
    cv2.putText(annotated_frame, f"FPS: {fps:.1f}", (10, 25), font, 0.6, (0, 255, 0), 2)
    cv2.putText(annotated_frame, f"Total Defects: {stats['total_defects_detected']}", (10, 50), font, 0.6, color, 1)
    cv2.putText(annotated_frame, f"Dents: {stats['dent']}", (10, 75), font, 0.5, color, 1)
    cv2.putText(annotated_frame, f"Dirt: {stats['dirt']}", (10, 100), font, 0.5, color, 1)
    cv2.putText(annotated_frame, f"Holes: {stats['hole']}", (10, 125), font, 0.5, color, 1)

    cv2.imshow("Live Package Defect Scanner", annotated_frame)

    # press 'x' to exit
    if cv2.waitKey(1 if INPUT_MODE != 'image' else 0) & 0xFF == ord('x') or INPUT_MODE == 'image':
        break

if cap:
    cap.release()
cv2.destroyAllWindows()