from src.counter import LineCounter


def main():

    counter = LineCounter(
        line_start=(220, 420),
        line_end=(1080, 420),
        direction="top_to_bottom",
        zone=10
    )

    # Vehicle starts clearly above the line
    print(counter.update(1, (500, 350)))

    # Vehicle still above the line
    print(counter.update(1, (500, 390)))

    # Vehicle enters the crossing zone
    print(counter.update(1, (500, 415)))

    # Vehicle clearly moves below the line
    print(counter.update(1, (500, 450)))

    # Same vehicle must not be counted again
    print(counter.update(1, (500, 470)))

    print()
    print("Final Count:", counter.count)


if __name__ == "__main__":
    main()