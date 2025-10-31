# Human Detection and Counting System

This project detects and counts humans in images, videos, or webcam feed using **YOLOv5** and displays results through a **Django** web interface.

---

## 🚀 Features
- Detects humans using YOLOv5 model
- Supports image, video, and real-time webcam input
- Displays detection results in a simple Django UI

---

## ⚙️ Setup Instructions

1. Clone the Repository
   ```bash
   git clone https://github.com/<your-username>/HUMAN_DETECTION_PROJECT.git
   cd HUMAN_DETECTION_PROJECT

2.Create virtual environment
  python -m venv venv
  venv\Scripts\activate   # On Windows

3.Install dependencies
  pip install -r requirements.txt

4.Download YOLO model weights
  Place your model file (e.g. yolov5su.pt) inside the models/ folder.

  Or download from YOLOv5 Releases 

5.Run the Django server
  python manage.py runserver




