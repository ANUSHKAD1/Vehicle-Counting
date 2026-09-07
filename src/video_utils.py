import cv2

VIDEO_PATH = "video/cars.mp4"


def get_video_info(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    duration = frame_count / fps if fps > 0 else 0

    cap.release()

    return {
        "width": width,
        "height": height,
        "fps": fps,
        "frame_count": frame_count,
        "duration": duration,
    }


def preview_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow("Vehicle Counting - Video Preview", frame)

        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    info = get_video_info(VIDEO_PATH)

    print("Video Information")
    print("------------------")
    print(f"Resolution : {info['width']} x {info['height']}")
    print(f"FPS        : {info['fps']}")
    print(f"Frames     : {info['frame_count']}")
    print(f"Duration   : {info['duration']:.2f} seconds")

    print("\nStarting video preview...")
    print("Press Q to close the preview.")

    preview_video(VIDEO_PATH)