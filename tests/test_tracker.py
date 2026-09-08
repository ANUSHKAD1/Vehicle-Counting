from src.tracker import VehicleTracker


def main():

    tracker = VehicleTracker()

    print("Allowed vehicle classes:")
    print(tracker.VEHICLE_CLASSES)

    print()

    # Expected vehicle classes
    expected = {
        "car",
        "truck",
        "bus",
        "motorcycle"
    }

    # Verify all required vehicle classes exist
    assert expected.issubset(
        tracker.VEHICLE_CLASSES
    )

    # Verify common non-vehicle classes are NOT allowed
    non_vehicle_classes = {
        "person",
        "bicycle",
        "cat",
        "dog"
    }

    for class_name in non_vehicle_classes:

        assert class_name not in tracker.VEHICLE_CLASSES

    print("Vehicle classes test: PASSED")
    print("Non-vehicle filtering test: PASSED")


if __name__ == "__main__":
    main()