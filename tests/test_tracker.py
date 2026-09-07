import cv2

from src.tracker import VehicleTracker


VIDEO_PATH = "video/cars.mp4"


def main():

    tracker = VehicleTracker()

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        raise ValueError("Could not open video")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        tracks = tracker.track(frame)

        for track in tracks:

            x1, y1, x2, y2 = map(int, track["bbox"])

            track_id = track["track_id"]
            class_name = track["class_name"]
            confidence = track["confidence"]

            label = f"{class_name} ID:{track_id} {confidence:.2f}"

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

        cv2.imshow("ByteTrack Vehicle Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()