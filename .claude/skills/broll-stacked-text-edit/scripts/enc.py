"""Video encoder choice: Apple VideoToolbox on a Mac, software x264/x265 elsewhere (Linux cloud sessions, Windows)."""
import sys

MAC = sys.platform == "darwin"


def venc(codec, rate):
    """codec 'hevc' or 'h264'; rate like '20M' or an int of bits/s. Returns ffmpeg output args."""
    if MAC:
        return ["-c:v", f"{codec}_videotoolbox", "-b:v", str(rate)] + (["-tag:v", "hvc1"] if codec == "hevc" else [])
    if codec == "hevc":
        return ["-c:v", "libx265", "-crf", "18", "-preset", "medium", "-tag:v", "hvc1", "-x265-params", "log-level=error"]
    return ["-c:v", "libx264", "-b:v", str(rate), "-maxrate", str(rate), "-bufsize", str(rate), "-preset", "medium", "-pix_fmt", "yuv420p"]
