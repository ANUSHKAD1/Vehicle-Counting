class LineCounter:

    def __init__(self, line_start, line_end, direction="top_to_bottom"):

        self.line_start = line_start
        self.line_end = line_end
        self.direction = direction

        self.count = 0

        # Stores the previous side of the line for every track
        self.previous_side = {}

        # Stores vehicles that have already been counted
        self.counted_ids = set()

    def get_side(self, center):

        x1, y1 = self.line_start
        x2, y2 = self.line_end

        px, py = center

        side = (x2 - x1) * (py - y1) - \
               (y2 - y1) * (px - x1)

        return side

    def update(self, track_id, center):

        current_side = self.get_side(center)

        crossed = False

        if track_id in self.previous_side:

            previous_side = self.previous_side[track_id]

            # Top -> Bottom
            if (
                previous_side < 0
                and current_side >= 0
                and track_id not in self.counted_ids
            ):
                self.count += 1
                self.counted_ids.add(track_id)
                crossed = True

        self.previous_side[track_id] = current_side

        return crossed