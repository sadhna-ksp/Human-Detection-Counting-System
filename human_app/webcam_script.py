import cv2
from .detection import detect  # adjust import if needed when calling from Django

def run_webcam_detection():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Starting webcam detection... Press 'q' to stop.")
    last_frame = None

    while True:
        success, frame = cap.read()
        if not success:
            print("Error: Failed to capture frame.")
            break

        frame = detect(frame)
        last_frame = frame
        cv2.imshow("Webcam Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save last frame to disk
    if last_frame is not None:
        output_path = "human_app/static/uploads/webcam_result.jpg"
        cv2.imwrite(output_path, last_frame)
        print(f"✅ Last frame saved to: {output_path}")
