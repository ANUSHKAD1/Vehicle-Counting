import cv2

from src.tracker import VehicleTracker
from src.counter import LineCounter


VIDEO_PATH = "video/cars.mp4"

LINE_START = (220, 420)
LINE_END = (1080, 420)


def process_video(video_path):

    tracker = VehicleTracker()

    counter = LineCounter(
        line_start=LINE_START,
        line_end=LINE_END,
        direction="top_to_bottom"
    )

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)

    frame_number = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_number += 1

        tracks = tracker.track(frame)

        # Draw counting line
        cv2.line(
            frame,
            LINE_START,
            LINE_END,
            (0, 0, 255),
            3
        )

        for track in tracks:

            x1, y1, x2, y2 = map(int, track["bbox"])

            track_id = track["track_id"]
            class_name = track["class_name"]
            confidence = track["confidence"]

            # Calculate vehicle center
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            crossed = counter.update(
                track_id,
                (center_x, center_y)
            )

            # Draw bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Draw center point
            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                (255, 0, 0),
                -1
            )

            # Label
            label = f"{class_name} ID:{track_id}"

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            # Show crossing alert
            if crossed:

                timestamp = frame_number / fps

                print(
                    f"Vehicle crossed | "
                    f"Time: {timestamp:.2f}s | "
                    f"Class: {class_name} | "
                    f"Track ID: {track_id}"
                )

                cv2.putText(
                    frame,
                    "VEHICLE COUNTED!",
                    (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (0, 0, 255),
                    3
                )

        # Display total count
        cv2.putText(
            frame,
            f"Total Count: {counter.count}",
            (50, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 255),
            3
        )

        cv2.imshow(
            "Vehicle Counting",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    print()
    print("Processing completed")
    print("-------------------")
    print(f"Total vehicles counted: {counter.count}")


if __name__ == "__main__":
    process_video(VIDEO_PATH)