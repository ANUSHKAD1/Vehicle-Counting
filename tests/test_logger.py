from src.logger import EventLogger


def main():

    logger = EventLogger("outputs/logs/test_events.csv")

    logger.log_event(
        video_name="cars.mp4",
        timestamp_seconds=12.34,
        event_type="vehicle_crossing",
        vehicle_class="car",
        track_id=7,
        direction="top_to_bottom"
    )

    logger.log_event(
        video_name="cars.mp4",
        timestamp_seconds=18.72,
        event_type="vehicle_crossing",
        vehicle_class="truck",
        track_id=12,
        direction="top_to_bottom"
    )

    logger.save()


if __name__ == "__main__":
    main()