import os
import pandas as pd
import streamlit as st

from src.processor import process_video


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Vehicle Flow Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SESSION STATE
# ============================================================

if "analysis_completed" not in st.session_state:
    st.session_state.analysis_completed = False


# ============================================================
# LAYOUT CONSTANTS  (single source of truth for uniform sizing)
# ============================================================

PANEL_RADIUS = 14
ROW_HEIGHT_TOP = 500      # Input Video / Run Analysis row
ROW_HEIGHT_MID = 460      # Distribution / Annotated Output row
KPI_HEIGHT = 108


# ============================================================
# PROFESSIONAL WHITE-SHADE THEME
# ============================================================

st.markdown(
    f"""
<style>
/* ---------- Global ---------- */

.stApp {{
    background: #fbfcfe;
    color: #182338;
}}

.main .block-container {{
    max-width: 1360px;
    padding-top: 1.25rem;
    padding-bottom: 3rem;
    padding-left: 2.4rem;
    padding-right: 2.4rem;
}}

div[data-testid="stVerticalBlock"] {{
    gap: 0.45rem;
}}

/* ---------- Typography baseline ---------- */

h3 {{
    font-size: 17px !important;
    font-weight: 800 !important;
    color: #172238 !important;
    letter-spacing: 0.1px;
    margin-bottom: 0 !important;
}}

[data-testid="stCaptionContainer"] {{
    color: #77859a !important;
    font-size: 13.5px !important;
}}

/* ---------- Hero ---------- */

.hero {{
    background: #ffffff;
    border: 1px solid #e3e9f1;
    border-left: 5px solid #2f6fed;
    border-radius: {PANEL_RADIUS + 2}px;
    padding: 21px 27px 20px 27px;
    margin-bottom: 20px;
    box-shadow: 0 5px 18px rgba(24, 45, 78, 0.045);
}}

.hero-kicker {{
    color: #2f6fed;
    font-size: 11.5px;
    font-weight: 800;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 5px;
}}

.hero-title {{
    color: #162238;
    font-size: 36px;
    line-height: 1.08;
    font-weight: 850;
    letter-spacing: -0.8px;
}}

.hero-title-accent {{
    color: #2f6fed;
}}

.hero-subtitle {{
    color: #6b7a90;
    font-size: 14.5px;
    line-height: 1.5;
    margin-top: 7px;
}}

/* ---------- Section headings (uniform across the whole page) ---------- */

.section-heading {{
    color: #172238;
    font-size: 21px;
    font-weight: 800;
    margin: 0;
}}

.section-copy {{
    color: #748197;
    font-size: 13.5px;
    margin-top: 2px;
    margin-bottom: 12px;
}}

/* ---------- Native Streamlit bordered containers = dashboard panels ---------- */

div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: #ffffff;
    border: 1px solid #e1e7ef;
    border-radius: {PANEL_RADIUS}px;
    box-shadow: 0 4px 15px rgba(24, 45, 78, 0.035);
}}

/* Vertically center each panel's content so mismatched content
   still looks balanced inside equal-height panels */
div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {{
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

/* Panels that hold a header + growing content (table panel) should
   align to the top instead of centering */
.panel-top > div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {{
    justify-content: flex-start;
}}

/* ---------- Video ---------- */

video {{
    border-radius: 9px !important;
    border: 1px solid #dfe6ef !important;
    box-shadow: 0 3px 12px rgba(24, 45, 78, 0.055);
    display: block;
    margin: 0 auto;
}}

/* ---------- Primary button ---------- */

.stButton > button {{
    background: #2f6fed;
    color: #ffffff;
    border: 1px solid #2f6fed;
    border-radius: 8px;
    min-height: 44px;
    font-size: 13px;
    font-weight: 750;
    box-shadow: 0 4px 12px rgba(47, 111, 237, 0.18);
}}

.stButton > button:hover {{
    background: #245dcc;
    border-color: #245dcc;
    color: #ffffff;
}}

/* ---------- Status pill ---------- */

.ready {{
    display: inline-block;
    background: #f1faf5;
    color: #237447;
    border: 1px solid #d2e9da;
    border-radius: 20px;
    padding: 5px 11px;
    font-size: 12.5px;
    font-weight: 700;
}}

/* ---------- Progress: percentage is ON the bar ---------- */

.progress-shell {{
    width: 100%;
    margin-top: 12px;
}}

.progress-track {{
    position: relative;
    width: 100%;
    height: 40px;
    background: #e8edf4;
    border: 1px solid #d8e0ea;
    border-radius: 9px;
    overflow: hidden;
}}

.progress-fill {{
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    background: #2f6fed;
    border-radius: 8px;
    transition: width 0.12s linear;
}}

.progress-number {{
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2;
    color: #243248;
    font-size: 15px;
    font-weight: 800;
}}

.progress-number.light {{
    color: #ffffff;
}}

.progress-meta {{
    color: #7a8799;
    font-size: 12.5px;
    margin-top: 6px;
}}

/* ---------- KPI cards (all identical height/padding) ---------- */

.kpi {{
    background: #ffffff;
    border: 1px solid #e1e7ef;
    border-radius: 12px;
    padding: 16px 18px;
    height: {KPI_HEIGHT}px;
    box-sizing: border-box;
    box-shadow: 0 3px 13px rgba(24, 45, 78, 0.035);
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.kpi-line {{
    width: 27px;
    height: 3px;
    background: #2f6fed;
    border-radius: 4px;
    margin-bottom: 11px;
}}

.kpi-label {{
    color: #78869a;
    font-size: 11.5px;
    font-weight: 750;
    letter-spacing: 0.7px;
    text-transform: uppercase;
}}

.kpi-value {{
    color: #172238;
    font-size: 28px;
    line-height: 1;
    font-weight: 850;
    margin-top: 7px;
}}

/* ---------- Table panel ---------- */

[data-testid="stDataFrame"] {{
    border: 1px solid #dfe6ee;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 3px 12px rgba(24, 45, 78, 0.035);
}}

/* ---------- Download ---------- */

.stDownloadButton > button {{
    background: #ffffff;
    color: #2f6fed;
    border: 1px solid #b9cae8;
    border-radius: 8px;
    min-height: 40px;
    font-weight: 700;
}}

.stDownloadButton > button:hover {{
    background: #f4f7fd;
    color: #245dcc;
}}

/* ---------- Dividers ---------- */

hr {{
    border: none;
    border-top: 1px solid #e5eaf1;
    margin: 22px 0;
}}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero">'
    '<div class="hero-kicker">COMPUTER VISION · TRAFFIC ANALYTICS</div>'
    '<div class="hero-title">Vehicle Flow <span class="hero-title-accent">Analytics</span></div>'
    '<div class="hero-subtitle">Vehicle detection, multi-object tracking and virtual-line crossing analysis for intelligent traffic monitoring.</div>'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-heading">Analysis</div>'
    '<div class="section-copy">Process the provided traffic footage and generate vehicle crossing events.</div>',
    unsafe_allow_html=True,
)

input_col, control_col = st.columns([1, 1], gap="medium")

# ============================================================
# INPUT VIDEO
# ============================================================

with input_col:
    with st.container(border=True, height=ROW_HEIGHT_TOP):
        st.subheader("Input Video")
        st.caption("Source traffic footage")

        video_path = "video/cars.mp4"

        if os.path.exists(video_path):
            st.video(video_path, width=620)
            st.caption("cars.mp4  ·  1280 × 720  ·  50 FPS  ·  60 seconds")
        else:
            st.error("Input video not found.")


# ============================================================
# RUN ANALYSIS
# ============================================================

with control_col:
    with st.container(border=True, height=ROW_HEIGHT_TOP):
        st.subheader("Run Analysis")

        if st.session_state.analysis_completed:
            st.markdown(
                '<span class="ready">✓ Analysis complete</span>',
                unsafe_allow_html=True,
            )
            st.caption("Latest analysis is ready.")
        else:
            st.markdown(
                '<span class="ready">● Ready to analyze</span>',
                unsafe_allow_html=True,
            )
            st.caption(
                "Detect vehicles, track movement and count valid top-to-bottom crossings."
            )

        st.write("")

        if st.button(
            "Run Vehicle Analysis",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.analysis_completed = False

            progress_placeholder = st.empty()
            status_placeholder = st.empty()

            try:

                def update_progress(
                    progress,
                    current_frame,
                    total_frames,
                    count,
                ):
                    percentage = max(0, min(100, int(progress * 100)))
                    text_class = "light" if percentage >= 50 else ""

                    progress_placeholder.markdown(
                        f'<div class="progress-shell">'
                        f'<div class="progress-track">'
                        f'<div class="progress-fill" style="width:{percentage}%;"></div>'
                        f'<div class="progress-number {text_class}">{percentage}%</div>'
                        f'</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                    status_placeholder.markdown(
                        f'<div class="progress-meta">'
                        f'Processing frame <strong>{current_frame:,}</strong> '
                        f'of <strong>{total_frames:,}</strong>'
                        f'&nbsp;&nbsp;·&nbsp;&nbsp;'
                        f'Vehicles counted: <strong>{count}</strong>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                total_count = process_video(
                    video_path,
                    show_window=False,
                    progress_callback=update_progress,
                )

                progress_placeholder.markdown(
                    '<div class="progress-shell">'
                    '<div class="progress-track">'
                    '<div class="progress-fill" style="width:100%;"></div>'
                    '<div class="progress-number light">100%</div>'
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )

                status_placeholder.success(
                    f"Analysis completed · {total_count} vehicles counted"
                )

                st.session_state.analysis_completed = True
                st.rerun()

            except Exception as e:
                st.error(f"Processing failed: {e}")


# ============================================================
# RESULTS
# ============================================================

event_log = "outputs/logs/events.csv"

if st.session_state.analysis_completed and os.path.exists(event_log):

    events = pd.read_csv(event_log)

    st.divider()

    st.markdown(
        '<div class="section-heading">Analysis Results</div>'
        '<div class="section-copy">Detected vehicles and recorded virtual-line crossing events.</div>',
        unsafe_allow_html=True,
    )

    total = len(events)
    cars = len(events[events["vehicle_class"] == "car"])
    trucks = len(events[events["vehicle_class"] == "truck"])
    buses = len(events[events["vehicle_class"] == "bus"])
    motorcycles = len(events[events["vehicle_class"] == "motorcycle"])

    # ========================================================
    # KPI ROW  (five identical-size cards)
    # ========================================================

    columns = st.columns(5, gap="medium")

    kpis = [
        ("Total Vehicles", total),
        ("Cars", cars),
        ("Trucks", trucks),
        ("Buses", buses),
        ("Motorcycles", motorcycles),
    ]

    for column, (label, value) in zip(columns, kpis):
        with column:
            st.markdown(
                f'<div class="kpi">'
                f'<div class="kpi-line"></div>'
                f'<div class="kpi-label">{label}</div>'
                f'<div class="kpi-value">{value}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ========================================================
    # DISTRIBUTION + ANNOTATED OUTPUT  (equal-height panels)
    # ========================================================

    st.divider()

    chart_col, video_col = st.columns([1, 1], gap="medium")

    with chart_col:
        with st.container(border=True, height=ROW_HEIGHT_MID):
            st.subheader("Vehicle Distribution")
            st.caption("Crossing events by vehicle type")

            chart_data = (
                events["vehicle_class"]
                .value_counts()
                .rename_axis("Vehicle")
                .reset_index(name="Count")
            )

            st.bar_chart(
                chart_data,
                x="Vehicle",
                y="Count",
                height=300,
            )

    with video_col:
        with st.container(border=True, height=ROW_HEIGHT_MID):
            st.subheader("Annotated Output")
            st.caption("Tracked vehicles and virtual crossing line")

            output_video = "outputs/videos/cars_annotated.mp4"

            if os.path.exists(output_video):
                st.video(output_video, width=520)
                st.caption("Bounding boxes · Track IDs · Crossing events")
            else:
                st.warning("Annotated output video not found.")

    # ========================================================
    # EVENT TABLE  (own panel, top-aligned, header + download inline)
    # ========================================================

    st.divider()

    st.markdown('<div class="panel-top">', unsafe_allow_html=True)
    with st.container(border=True):
        header_col, download_col = st.columns([3.5, 1], gap="large")

        with header_col:
            st.subheader("Vehicle Crossing Events")
            st.caption(f"{len(events)} valid crossing events recorded")

        with download_col:
            with open(event_log, "rb") as file:
                st.download_button(
                    "Download Event Log",
                    data=file,
                    file_name="vehicle_events.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

        display_events = events[
            [
                "timestamp_seconds",
                "vehicle_class",
                "track_id",
                "direction",
            ]
        ].copy()

        display_events.rename(
            columns={
                "timestamp_seconds": "Time (sec)",
                "vehicle_class": "Vehicle",
                "track_id": "Track ID",
                "direction": "Direction",
            },
            inplace=True,
        )

        display_events["Direction"] = display_events["Direction"].replace(
            {"top_to_bottom": "Top → Bottom"}
        )

        display_events.index = range(1, len(display_events) + 1)
        display_events.index.name = "#"

        st.dataframe(
            display_events,
            use_container_width=True,
            height=460,
            hide_index=False,
        )
    st.markdown('</div>', unsafe_allow_html=True)