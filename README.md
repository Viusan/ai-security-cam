# AI Security Camera

A Raspberry Pi-based security camera that uses YOLOv8 to detect people in a live video feed, face recognition (built on dlib) to identify known faces, and sends instant photo alerts via Telegram.

`test_bot_pi.py` is the main script which runs the camera, YOLO detection, face recognition, and Telegram alerting loop.

It works by using a USB camera which continuously captures frames, and each frame is run through a YOLOv8n model for object detection. Detected objects are filtered for the person class (class id 0). When a person is detected, the current frame is saved, and a facial encoding is generated from it and compared against a pre-stored encoding of a known face. The result of that comparison determines the alert. If it matches, the photo is sent to Telegram captioned as a recognized person and if not, it's sent captioned as an unknown person. A cooldown timer of 20 seconds prevents repeated alerts from the same continuous detection.

> **Note:** Facial recognition (`dlib`) has currently only been built and tested on Windows using a conda environment.

## Hardware used

- Raspberry Pi 5 (8GB)
- Official Raspberry Pi case with integrated cooling (SC1160/SC1159)
- 27W USB-C power adapter (5V/5A PD)
- microSD card (64GB)
- USB webcam

## Software/Tech Stack

- Python 3
- OpenCV — camera capture and frame handling
- Ultralytics YOLOv8 — object detection (`yolov8n.pt`)
- face_recognition (built on Dlib) — face detection, encoding, and comparison for identity matching
- python-telegram-bot — sending Telegram alerts
- python-dotenv — loading variables from a `.env` file

## Setup

1. Clone the repository

2. Create a Telegram bot
   - Message @BotFather on Telegram to create a bot and get a bot token.
   - Get your personal chat ID (e.g. by messaging @userinfobot).

3. Configure environment variables

   Create a `.env` file in the project root:
   ```
   TOKEN=your_telegram_bot_token
   CHAT_ID=your_telegram_chat_id
   ```

4. Add a reference photo

   Save a clear, front-facing photo of the person you want recognized as `viusan.jpg` in the project root (or update the filename referenced at the top of `test_bot_pi.py`). This photo is used to generate the known face encoding that live detections are compared against.

5. Set up a virtual environment and install dependencies

   On Raspberry Pi OS (Bookworm), a virtual environment is required since the system blocks global pip install by default.
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install ultralytics opencv-python python-telegram-bot python-dotenv face_recognition
   ```

   **Installing `dlib`/`face_recognition`:**
   - On Windows, `dlib` frequently fails to build via plain `pip install` (no pre-built wheel available). The most reliable route is installing it through a conda environment instead: `conda install -c conda-forge dlib`, then `pip install face_recognition` on top.
   - On Raspberry Pi OS, `dlib` has no pre-built wheel for ARM64 and must compile from source, which can take 40+ minutes and risks running out of memory. If attempting this on-device, temporarily increasing your swap file size (to ~4GB) beforehand is recommended.

6. Run it
   ```
   python3 test_bot_pi.py
   ```

   Note: When running headless over SSH (no monitor attached), comment out the `cv2.imshow()` and the `cv2.waitKey('q')` exit check in `test_bot_pi.py`. There's no display to render a window on, and the script will otherwise fail or hang. Stop the script with `Ctrl+C` instead.

## Configuration

- **Detection cooldown**: adjust the `20` second threshold in `test_bot_pi.py` to control how often alerts can be sent.
- **Known face**: swap `viusan.jpg` for a different reference photo to recognize a different person.

## Known Issues / Challenges

A few notable bugs hit during development, documented for reference:

- **`numpy 2.0` / `dlib` incompatibility** — face recognition failed with `RuntimeError: Unsupported image type, must be 8bit gray or RGB image` despite valid image data. It was caused by a compatibility break between `numpy 2.0+` and the installed `dlib` build. Fixed by pinning `numpy<2`.
