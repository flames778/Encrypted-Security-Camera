import time
import datetime
import subprocess
import cv2
import queue
import threading
from config import *
from key_manager import get_or_create_key
from encrypt_chunk import encrypt_chunk
from motion import MotionDetector

def ffmpeg_worker(frame_queue: queue.Queue, key: bytes, width: int, height: int, fps: float, start_time_str: str):
    """
    Reads frames from the queue, pipes them to ffmpeg to encode as raw H.264,
    encrypts the output, and saves to disk.
    """
    # ffmpeg command to accept raw frames and output H.264
    command = [
        'ffmpeg',
        '-y', # overwrite
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-s', f'{width}x{height}',
        '-pix_fmt', 'bgr24',
        '-r', str(fps),
        '-i', '-', # read from stdin
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-tune', 'zerolatency',
        '-f', 'h264',
        '-' # output to stdout
    ]
    
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    
    # Thread to push frames to ffmpeg
    def push_frames():
        try:
            while True:
                frame = frame_queue.get()
                if frame is None: # Sentinel
                    break
                process.stdin.write(frame.tobytes())
        except (BrokenPipeError, ValueError):
            pass
        finally:
            if process.stdin:
                try:
                    process.stdin.close()
                except Exception:
                    pass
                
    t = threading.Thread(target=push_frames)
    t.start()
    
    # Read output H.264 from ffmpeg
    h264_data = process.stdout.read()
    process.wait()
    t.join()
    
    if len(h264_data) > 0:
        print(f"Encrypting chunk: {len(h264_data)} bytes of H.264 video.")
        encrypted = encrypt_chunk(h264_data, key)
        filepath = FOOTAGE_DIR / f"{start_time_str}.enc"
        with open(filepath, "wb") as f:
            f.write(encrypted)
        print(f"Saved chunk: {filepath}")

def main():
    print("Starting Encrypted Security Camera...")
    key = get_or_create_key()
    print("Encryption key loaded successfully.")
    
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Try to set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUTION[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUTION[1])
    
    # Get actual resolution
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    if actual_fps <= 0:
        actual_fps = FPS
        
    print(f"Webcam opened at {width}x{height} @ {actual_fps} fps")
    
    detector = MotionDetector(threshold=MOTION_THRESHOLD)
    
    recording = False
    motion_cooldown_timer = 0
    chunk_start_time = 0
    frame_queue = None
    worker_thread = None
    start_time_str = ""

    print("Listening for motion... (Press Ctrl+C to stop)")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame.")
                time.sleep(0.1)
                continue
                
            current_time = time.time()
            
            # Motion Detection
            if ENABLE_MOTION_DETECTION:
                has_motion = detector.detect(frame)
                if has_motion:
                    motion_cooldown_timer = current_time + MOTION_COOLDOWN
                    if not recording:
                        print("Motion detected! Started recording.")
            else:
                motion_cooldown_timer = current_time + 1 # always "detecting"
                
            if current_time < motion_cooldown_timer:
                if not recording:
                    recording = True
                    chunk_start_time = current_time
                    start_time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    frame_queue = queue.Queue()
                    worker_thread = threading.Thread(target=ffmpeg_worker, args=(frame_queue, key, width, height, actual_fps, start_time_str))
                    worker_thread.start()
                    
                # Put frame into current chunk
                frame_queue.put(frame)
                
                # Check if chunk duration is reached
                if current_time - chunk_start_time >= CHUNK_DURATION:
                    # Finalize current chunk
                    frame_queue.put(None)
                    worker_thread = None
                    recording = False
            else:
                if recording:
                    print("Motion stopped. Ending recording.")
                    frame_queue.put(None)
                    worker_thread = None
                    recording = False
                    
            # Small sleep to yield
            time.sleep(1 / (actual_fps * 2))
            
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        if recording and frame_queue:
            frame_queue.put(None)
        cap.release()

if __name__ == "__main__":
    main()
