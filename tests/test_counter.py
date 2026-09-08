from src.counter import LineCounter


def test_single_vehicle_crossing():

    counter = LineCounter(
        line_start=(220, 420),
        line_end=(1080, 420),
        direction="top_to_bottom",
        zone=10
    )

    track_id = 1

    # Vehicle starts above the line
    counter.update(track_id, (500, 350))

    # Vehicle crosses the line
    crossed = counter.update(track_id, (500, 450))

    assert crossed is True
    assert counter.count == 1

    print("Test A - Single vehicle crossing: PASSED")


def test_vehicle_does_not_cross():

    counter = LineCounter(
        line_start=(220, 420),
        line_end=(1080, 420),
        direction="top_to_bottom",
        zone=10
    )

    track_id = 2

    # Vehicle remains above the line
    counter.update(track_id, (500, 350))
    counter.update(track_id, (500, 360))
    counter.update(track_id, (500, 380))

    assert counter.count == 0

    print("Test B - Vehicle does not cross: PASSED")


def test_multiple_vehicles():

    counter = LineCounter(
        line_start=(220, 420),
        line_end=(1080, 420),
        direction="top_to_bottom",
        zone=10
    )

    # Vehicle 1
    counter.update(1, (500, 350))
    counter.update(1, (500, 450))

    # Vehicle 2
    counter.update(2, (600, 350))
    counter.update(2, (600, 450))

    # Vehicle 3
    counter.update(3, (700, 350))
    counter.update(3, (700, 450))

    assert counter.count == 3

    print("Test C - Multiple vehicles: PASSED")


def test_duplicate_count_prevention():

    counter = LineCounter(
        line_start=(220, 420),
        line_end=(1080, 420),
        direction="top_to_bottom",
        zone=10
    )

    track_id = 10

    # Vehicle approaches from above
    counter.update(track_id, (500, 350))

    # First crossing
    counter.update(track_id, (500, 450))

    # Vehicle continues below
    counter.update(track_id, (500, 500))

    # Vehicle moves back toward the line
    counter.update(track_id, (500, 390))

    # Crosses again
    counter.update(track_id, (500, 450))

    assert counter.count == 1

    print("Test D - Duplicate count prevention: PASSED")


def main():

    test_single_vehicle_crossing()
    test_vehicle_does_not_cross()
    test_multiple_vehicles()
    test_duplicate_count_prevention()

    print()
    print("All counter robustness tests: PASSED")


if __name__ == "__main__":
    main()