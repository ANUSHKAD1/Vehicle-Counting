import cv2
import os

from src.tracker import VehicleTracker
from src.counter import LineCounter
from src.logger import EventLogger

VIDEO_PATH = "video/cars.mp4"
OUTPUT_VIDEO_PATH = "outputs/videos/cars_annotated.mp4"

LINE_START = (220, 420)
LINE_END = (1080, 420)


def process_video(video_path):

    tracker = VehicleTracker()

    counter = LineCounter(
        line_start=LINE_START, line_end=LINE_END, direction="top_to_bottom"
    )

    logger = EventLogger("outputs/logs/events.csv")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    os.makedirs("outputs/videos", exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        OUTPUT_VIDEO_PATH,
        fourcc,
        fps,
        (width, height)
    )

    if not writer.isOpened():
        raise ValueError(
            f"Could not create output video: {OUTPUT_VIDEO_PATH}"
        )

    frame_number = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_number += 1

        tracks = tracker.track(frame)

        # Draw counting line
        cv2.line(frame, LINE_START, LINE_END, (0, 0, 255), 3)

        for track in tracks:

            x1, y1, x2, y2 = map(int, track["bbox"])

            track_id = track["track_id"]
            class_name = track["class_name"]
            confidence = track["confidence"]

            # Calculate vehicle center
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            crossed = counter.update(track_id, (center_x, center_y))

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Draw center point
            cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)

            # Vehicle label
            label = f"{class_name} ID:{track_id} {confidence:.2f}"

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

            # Vehicle crossed the line
            if crossed:

                timestamp = frame_number / fps

                print(
                    f"Vehicle crossed | "
                    f"Time: {timestamp:.2f}s | "
                    f"Class: {class_name} | "
                    f"Track ID: {track_id}"
                )

                logger.log_event(
                    video_name="cars.mp4",
                    timestamp_seconds=timestamp,
                    event_type="vehicle_crossing",
                    vehicle_class=class_name,
                    track_id=track_id,
                    direction="top_to_bottom",
                )

                cv2.putText(
                    frame,
                    "VEHICLE COUNTED!",
                    (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (0, 0, 255),
                    3,
                )

        # Display total count
        cv2.putText(
            frame,
            f"Total Count: {counter.count}",
            (50, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 255),
            3,
        )
        
        writer.write(frame)
        cv2.imshow("Vehicle Counting", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release video resources
    cap.release()
    writer.release()
    cv2.destroyAllWindows()

    # Save all crossing events
    logger.save()

    print()
    print("Processing completed")
    print("-------------------")
    print(f"Total vehicles counted: " f"{counter.count}")


if __name__ == "__main__":
    process_video(VIDEO_PATH)
