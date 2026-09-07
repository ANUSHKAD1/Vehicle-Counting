import csv
import os


class EventLogger:

    def __init__(self, output_path):
        self.output_path = output_path

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        self.events = []

    def log_event(
        self,
        video_name,
        timestamp_seconds,
        event_type,
        vehicle_class,
        track_id,
        direction
    ):

        event = {
            "video_name": video_name,
            "timestamp_seconds": round(timestamp_seconds, 2),
            "event_type": event_type,
            "vehicle_class": vehicle_class,
            "track_id": track_id,
            "direction": direction
        }

        self.events.append(event)

    def save(self):

        fieldnames = [
            "video_name",
            "timestamp_seconds",
            "event_type",
            "vehicle_class",
            "track_id",
            "direction"
        ]

        with open(
            self.output_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(self.events)

        print(f"Event log saved to: {self.output_path}")