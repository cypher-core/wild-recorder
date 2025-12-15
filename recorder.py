
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
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_file = os.path.join(ARCHIVE_DIR, f"{timestamp}.mp4")

        ffmpeg_command = [
            "ffmpeg",
            "-rtsp_transport", "tcp",
            "-i", RTSP_URL,
            "-c", "copy",
            "-map", "0",
            "-f", "segment",
            "-segment_time", "60",
            "-segment_format", "mp4",
            "-reset_timestamps", "1",
            output_file,
        ]

        try:
            print(f"Starting recording... output to {output_file}")
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
