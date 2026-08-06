# AI Security Camera

A Raspberry Pi-based security camera that uses YOLOv8 to detect people in a live video feed and sends instant photo alerts to Telegram.

`test_bot_pi.py` is the main script which runs the camera, YOLO detection, and Telegram alerting loop.

It works by using a USB camera which continuously captures frames, and each frame is run through a YOLOv8n model for object detection. Detected objects are filtered for the person class, which has class id 0, and when a person is detected the current frame is saved and sent as a photo to a Telegram chat via a bot. A cooldown timer of 20 seconds is added to prevent repeated alerts from the same continuous detection.

## Hardware used

- Raspberry Pi 5 (8GB)
- Official Raspberry Pi case with integrated cooling (SC1160/SC1159)
- 27W USB-C power adapter (5V/5A PD)
- microSD card (64GB)
- USB webcam

## Software/Tech Stack

- Python3
- OpenCV — camera capture and frame handling
- Ultralytics YOLOv8 — object detection (yolov8n.pt)
- python-telegram-bot — sending Telegram alerts
- python-dotenv — loading variables from a .env file

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

4. Set up a virtual environment and install dependencies

   On Raspberry Pi OS (Bookworm), a virtual environment is required since the system blocks global pip install by default.
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install ultralytics opencv-python python-telegram-bot python-dotenv
   ```

5. Run it
   ```
   python3 test_bot_pi.py
   ```

   Note: When running headless over SSH (no monitor attached), comment out the `cv2.imshow()` and the `cv2.waitKey('q')` exit check in `test_bot_pi.py`. There's no display to render a window on, and the script will otherwise fail or hang. Stop the script with `Ctrl+C` instead.
