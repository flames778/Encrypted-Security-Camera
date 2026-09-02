# Encrypted Security Camera

A privacy-focused security camera application that runs natively on macOS (and can be ported to Linux/Raspberry Pi). It captures video from your webcam, splits it into fixed-length chunks, encrypts each chunk using AES-256-GCM, and saves it to disk. No plaintext video is ever stored.

## Features
- **AES-256-GCM Encryption**: Provides both confidentiality and authenticity. Video chunks cannot be read or tampered with without the key.
- **Chunk-Based Storage**: Video is saved in 10-second encrypted chunks (`.enc`), enabling easy partial decryption.
- **Motion Detection**: Uses OpenCV background subtraction to only record when movement is detected, saving storage space.
- **Raw H.264 Video**: Uses `ffmpeg` to pipe raw frames directly into an H.264 stream, allowing seamless merging of multiple video chunks.

## Prerequisites
- macOS (Intel or Apple Silicon)
- Python 3.9+
- `ffmpeg` installed via Homebrew

## Setup Instructions

1. **Install ffmpeg:**
   ```bash
   brew install ffmpeg
   ```

2. **Clone the repository and enter the directory:**
   ```bash
   git clone https://github.com/flames778/Encrypted-Security-Camera.git
   cd Encrypted-Security-Camera
   ```

3. **Set up a virtual environment and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install opencv-python cryptography numpy
   ```

## Usage

### 1. Start Recording
Run the main script to start the security camera:
```bash
python main.py
```
- On the first run, a new AES-256 key will be generated and saved to `keys/video_key.bin`. **Keep this safe!**
- The camera will watch for motion. When motion is detected, it will start recording and saving `.enc` files in the `footage/` directory.
- Press `Ctrl+C` to stop.

### 2. Decrypt a Single Chunk
You can decrypt a specific `.enc` file back to `.h264` using the decrypt tool:
```bash
python decrypt.py footage/<timestamp>.enc out.h264
```
You can then play the video using `ffplay`:
```bash
ffplay out.h264
```

### 3. Decrypt and Merge All Chunks
To decrypt all chunks in the `footage/` directory and merge them into a single continuous video:
```bash
python batch_decrypt.py merged.h264
```

You can then play the combined video using `ffplay`:
```bash
ffplay merged.h264
```
*(Alternatively, you can drag and drop `merged.h264` into VLC Media Player or another supported video player).*

## Security Notes
- **Key Management**: The encryption key (`keys/video_key.bin`) is stored locally. If this key is lost, all recorded footage becomes permanently unrecoverable. 
- **Authentication**: AES-GCM guarantees both the secrecy and the integrity of the footage. Any modification to a `.enc` file will cause the authentication tag check to fail during decryption.
- **Git Ignore**: The `keys/` and `footage/` directories are explicitly ignored by `.gitignore` to prevent accidentally uploading your key or encrypted videos.

## Future Improvements
- **Encrypted Live Streaming**: Build a small HTTPS server to stream `.enc` chunks to a browser, which decrypts them on-the-fly using WebCrypto.
- **Key on USB**: Store the key on a physical USB drive. The camera will only record/decrypt if the specific USB drive is mounted.
- **Cloud Auto-Upload**: Safely upload encrypted chunks to a cloud provider like S3 or Google Drive. Since they are encrypted, the cloud provider cannot view the footage.
- **Raspberry Pi Deployment**: Swap the OpenCV webcam capture with the Pi Camera module.

- This project is actively being developed and improved.
