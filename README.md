Markdown
# Automated Package Defect Detector

An automated quality control system built with Python, YOLO, and OpenCV. This project simulates a conveyor belt scanner that identifies damaged cardboard boxes in real-time. It detects three specific types of defects: **dents**, **dirt**, and **holes**.

# Features
* **Multi-Source Input:** Seamlessly switch between `webcam` for live scanning, `video` for recorded footage, and `image` for static testing.
* **Real-Time HUD:** Displays a live on-screen overlay showing the current FPS and a statistics panel tracking exact defect counts.
* **Automated Logging:** Automatically saves raw screenshots of defective packages into a `detected_defects` directory the moment a flaw is scanned.
* **Lightweight Custom Model:** Uses a highly efficient, custom-trained YOLO model included directly in the repository.

# Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/package-defect-detector.git](https://github.com/YOUR_USERNAME/package-defect-detector.git)
   cd package-defect-detector
Install dependencies:
Ensure you have Python installed, then run:

Bash
pip install -r requirements.txt

**Usage**
Open main.py and modify the INPUT_MODE and INPUT_PATH variables at the top of the file to choose your testing source.

Python
# --- CONFIGURATION ---
INPUT_MODE = 'image'              # Options: 'webcam', 'video', or 'image'
INPUT_PATH = 'test_box_01.png'    # Path to your test file
Run the scanner:

Bash
python main.py
Controls
Live Webcam/Video: Press x on your keyboard to stop the feed and close the window.

Static Image: Press any key to close the window.

📁 Project Structure
main.py: The main execution script containing the detection loop, HUD drawing, and screenshot logic.

frame_extractor.py: Utility script for extracting frames from video (if applicable).

models/: Contains the custom-trained YOLO weights (package_defect_v2.pt).

requirements.txt: Required Python libraries.