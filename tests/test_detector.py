import cv2

from src.detector import VehicleDetector


VIDEO_PATH = "video/cars.mp4"


def main():

    detector = VehicleDetector()

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        raise ValueError("Could not open video")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        detections = detector.detect(frame)

        for detection in detections:

            x1, y1, x2, y2 = map(int, detection["bbox"])

            class_name = detection["class_name"]
            confidence = detection["confidence"]

            label = f"{class_name} {confidence:.2f}"

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        cv2.imshow("YOLO Vehicle Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()