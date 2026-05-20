import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
KEYS_DIR = BASE_DIR / "keys"
FOOTAGE_DIR = BASE_DIR / "footage"

# Ensure directories exist
KEYS_DIR.mkdir(exist_ok=True)
FOOTAGE_DIR.mkdir(exist_ok=True)

# Key file path
KEY_FILE = KEYS_DIR / "video_key.bin"

# Camera Settings
CAMERA_INDEX = 0
RESOLUTION = (1280, 720) # 720p
FPS = 20.0

# Recording Settings
CHUNK_DURATION = 10 # seconds

# Motion Detection Settings
ENABLE_MOTION_DETECTION = True
MOTION_THRESHOLD = 5000  # Number of changed pixels to trigger motion
MOTION_COOLDOWN = 10 # Keep recording for 10 seconds after motion stops
