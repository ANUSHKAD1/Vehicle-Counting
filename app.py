import streamlit as st
import os

from src.processor import process_video


st.set_page_config(
    page_title="Vehicle Counting & Flow Analysis",
    page_icon="🚗",
    layout="wide"
)


st.title("🚗 Vehicle Counting & Flow Analysis")

st.write(
    "Detect, track, and count vehicles crossing the predefined virtual line."
)


st.divider()


# -----------------------------
# Input video
# -----------------------------

st.subheader("Input Video")

video_path = "video/cars.mp4"

if os.path.exists(video_path):
    st.video(video_path)
else:
    st.error("Input video not found.")


# -----------------------------
# Run analysis
# -----------------------------

st.subheader("Vehicle Analysis")

if st.button("▶ Run Vehicle Counting", type="primary"):

    progress_bar = st.progress(0)

    status_text = st.empty()

    try:

        def update_progress(progress, current_frame, total_frames, count):
            progress_bar.progress(progress)

            percentage = int(progress * 100)

            status_text.text(
                f"Processing video... {percentage}% "
                f"({current_frame}/{total_frames} frames) | "
                f"Vehicles counted: {count}"
            )

        total_count = process_video(
            video_path,
            show_window=False,
            progress_callback=update_progress
        )

        progress_bar.progress(1.0)

        status_text.success(
            f"Processing completed! Total vehicles counted: {total_count}"
        )

        st.metric(
            label="Total Vehicles Counted",
            value=total_count
        )

    except Exception as e:
        st.error(f"Processing failed: {e}")


# -----------------------------
# Output video
# -----------------------------

output_video = "outputs/videos/cars_annotated.mp4"

if os.path.exists(output_video):

    st.divider()

    st.subheader("Annotated Output")

    st.video(output_video)


# -----------------------------
# Event log
# -----------------------------

event_log = "outputs/logs/events.csv"

if os.path.exists(event_log):

    st.divider()

    st.subheader("Vehicle Crossing Events")

    import pandas as pd

    events = pd.read_csv(event_log)

    # Create a clean table for display
    display_events = events[
        [
            "timestamp_seconds",
            "vehicle_class",
            "track_id",
            "direction"
        ]
    ].copy()

    # Rename columns
    display_events.rename(
        columns={
            "timestamp_seconds": "Time (sec)",
            "vehicle_class": "Vehicle",
            "track_id": "Track ID",
            "direction": "Direction"
        },
        inplace=True
    )

    # Convert direction to a more readable format
    display_events["Direction"] = display_events["Direction"].replace(
        {
            "top_to_bottom": "Top → Bottom"
        }
    )

    # Start table index from 1 instead of 0
    display_events.index = range(1, len(display_events) + 1)
    display_events.index.name = "No."

    st.dataframe(
        display_events,
        use_container_width=True
    )