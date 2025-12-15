# Wild Recorder Service

A dedicated service to continuously record and archive the RTSP video stream from the `wild-spider` project.

## Configuration

This service requires the following environment variable to be set in a `.env` file:

- `RTSP_URL`: The full RTSP stream URL for the camera feed.

Example `.env` file:
```
RTSP_URL="rtsp://user:password@camera_ip/live"
```

## Running Locally

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the service:
   ```bash
   python recorder.py
   ```
The service will start recording the stream into timestamped video segments in the `archive/` directory.
