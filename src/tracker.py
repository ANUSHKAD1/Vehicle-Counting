from ultralytics import YOLO


class VehicleTracker:

    VEHICLE_CLASSES = {
        "car",
        "truck",
        "bus",
        "motorcycle"
    }

    def __init__(self, model_path="yolo11n.pt", confidence=0.40):
        self.model = YOLO(model_path)
        self.confidence = confidence

    def track(self, frame):

        results = self.model.track(
            frame,
            conf=self.confidence,
            persist=True,
            tracker="bytetrack.yaml",
            verbose=False
        )

        tracks = []

        for result in results:

            if result.boxes.id is None:
                continue

            boxes = result.boxes.xyxy.cpu().tolist()
            track_ids = result.boxes.id.int().cpu().tolist()
            class_ids = result.boxes.cls.int().cpu().tolist()
            confidences = result.boxes.conf.cpu().tolist()

            for bbox, track_id, class_id, confidence in zip(
                boxes,
                track_ids,
                class_ids,
                confidences
            ):

                class_name = self.model.names[class_id]

                # Ignore people and other non-vehicle objects
                if class_name not in self.VEHICLE_CLASSES:
                    continue

                tracks.append({
                    "bbox": bbox,
                    "track_id": track_id,
                    "class_id": class_id,
                    "class_name": class_name,
                    "confidence": confidence
                })

        return tracks