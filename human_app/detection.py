import os
import cv2
import imutils
from ultralytics import YOLO

model = YOLO("yolov5s.pt")

def detect(frame):
    results = model(frame)
    person_count = 0
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model.names[int(box.cls[0])]
            if label == "person":
                person_count += 1
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'Person {person_count}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.putText(frame, f'Total Persons: {person_count}', (40, 40),
                cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
    return frame

def detect_by_image(path, output_path):
    image = cv2.imread(path)
    if image is None:
        print("Error: Image not found.")
        return None
    image = imutils.resize(image, width=min(800, image.shape[1]))
    result_image = detect(image)
    if output_path:
        cv2.imwrite(output_path, result_image)
    return output_path

def detect_by_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error: Cannot open video.")
        return None

    success, frame = cap.read()
    if not success:
        print("Error: Cannot read video.")
        return None

    frame = imutils.resize(frame, width=min(800, frame.shape[1]))
    height, width = frame.shape[:2]

    output_path = os.path.splitext(output_path)[0] + '.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, 10, (width, height))

    frame = detect(frame)
    writer.write(frame)

    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = imutils.resize(frame, width=width)
        frame = detect(frame)
        writer.write(frame)

    cap.release()
    writer.release()
    cv2.destroyAllWindows()

    return output_path
