
import os
import subprocess
import time
from dotenv import load_dotenv

load_dotenv()

RTSP_URL = os.getenv("RTSP_URL")
ARCHIVE_DIR = "archive"


def record_stream():
    """
    Continuously records the RTSP stream in 1-minute segments.
    """
    if not RTSP_URL:
        print("RTSP_URL not found in environment variables.")
        return

    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)

    while True:
        ffmpeg_command = [
            "ffmpeg",
            "-rtsp_transport", "tcp",
            "-i", RTSP_URL,
            "-c", "copy",
            "-map", "0",
            "-f", "segment",
            "-segment_time", "60",
            "-segment_format", "mp4",
            "-strftime", "1",
            "-reset_timestamps", "1",
            os.path.join(ARCHIVE_DIR, "%Y%m%d-%H%M%S.mp4"),
        ]

        try:
            print(f"Starting recording... output to {ARCHIVE_DIR}/%Y%m%d-%H%M%S.mp4")
            subprocess.run(ffmpeg_command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"ffmpeg command failed with exit code {e.returncode}")
            print(f"ffmpeg stderr: {e.stderr}")
            time.sleep(5)  # Wait 5 seconds before retrying
        except FileNotFoundError:
            print("ffmpeg not found. Please ensure ffmpeg is installed and in your PATH.")
            break


if __name__ == "__main__":
    record_stream()
