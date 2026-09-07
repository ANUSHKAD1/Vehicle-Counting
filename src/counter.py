class LineCounter:
    def __init__(self, line_start, line_end, direction="top_to_bottom", zone=10):
        self.line_start = line_start
        self.line_end = line_end
        self.direction = direction
        self.zone = zone

        self.count = 0
        self.counted_ids = set()

        # Store whether each vehicle has clearly been above the line
        self.track_state = {}

    def update(self, track_id, center):
        center_x, center_y = center

        line_y = self.line_start[1]
        crossed = False

        # Create state for a new vehicle
        if track_id not in self.track_state:
            self.track_state[track_id] = {
                "has_been_above": False
            }

        state = self.track_state[track_id]

        # Vehicle is clearly above the line
        if center_y <= line_y - self.zone:
            state["has_been_above"] = True

        # Vehicle has moved clearly below the line
        if (
            self.direction == "top_to_bottom"
            and state["has_been_above"]
            and center_y >= line_y + self.zone
            and track_id not in self.counted_ids
        ):
            self.count += 1
            self.counted_ids.add(track_id)
            crossed = True

        return crossed