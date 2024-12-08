🚗 Lane Detection System
This repository contains a Lane Detection System that identifies lanes in a video or image feed. It features a web-based front-end to showcase the detection results and the ratio of detected lanes. The back-end uses Python with the OpenCV library for lane detection.

📌 Features
Front-End Website:

Displays detection results.
Shows the ratio of detected lanes for better analysis.
Back-End:

Developed in Python.
Utilizes the OpenCV library for image and video processing.
Detects lanes in real-time or from pre-recorded inputs.

Lane-Detection-System/
│
├── frontend/                # Contains front-end website files (HTML, CSS, JS)
│   ├── index.html           # Main webpage
│   ├── style.css            # CSS for styling
│   └── script.js            # JavaScript logic (if applicable)
│
├── backend/                 # Contains back-end logic
│   ├── lane_detection.py    # Main Python script for lane detection
│   └── utils.py             # Helper functions for lane processing
│
├── media/                   # Sample images or videos
│   ├── sample_input.mp4     # Sample video input for testing
│   └── output_demo.png      # Screenshot of detection output
│
├── requirements.txt         # Required Python dependencies
└── README.md                # Documentation (this file)

🚀 How It Works

Input:
Video feed or images are passed into the backend.
Sample videos are provided in the media/ folder.

Lane Detection:
The Python backend processes the input using OpenCV to detect lanes.
Detected lanes are overlaid on the original input.

Output:
The front-end website displays:
Video/image results with detected lanes.
Detection ratio (percentage of lanes successfully detected).

💻 Technologies Used
Python (Backend)
OpenCV (Computer Vision)
HTML/CSS/JavaScript (Front-End)

🔧 Future Improvements
Real-time lane detection using webcam feeds.
Lane curve prediction for autonomous driving systems.
Integration of a Flask/Django server to connect front-end with backend dynamically.
