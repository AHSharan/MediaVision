# MediaVision
MediaVision is a Python application that leverages MediaPipe and OpenCV for hand gesture recognition to control media playback and system volume. Using a webcam, the program detects specific hand gestures to perform actions such as play/pause, next track, previous track, and volume adjustment.
## Features
- Play/Pause: Tap the thumb and middle finger together to play or pause the media.
- Next Track: Swipe your thumb to the right while maintaining a specific hand gesture to skip to the next track.
- Previous Track: Swipe your thumb to the left while maintaining a specific hand gesture to go to the previous track.
- Volume Control: Adjust the system volume by moving your hand up and down while holding a gesture.
## Requirements
- Python 3.x
- OpenCV
- MediaPipe
- PyAutoGUI
- PyCaw

#Installation
Clone the repository:

git clone https://github.com/ahsharan/MediaVision.git
cd MediaVision

Install the required dependencies:

pip install opencv-python mediapipe pyautogui pycaw comtypes
# Usage
Run the script:
python mediavision.py
Ensure your webcam is connected.
Use the specified hand gestures in front of the webcam to control media playback and adjust the volume.
# How It Works
Hand Tracking: Uses MediaPipe to detect and track hand landmarks in real-time.
Gesture Recognition: Identifies specific gestures based on the relative positions of finger tips.
Media Control: Uses PyAutoGUI to send media control commands (play/pause, next track, previous track) based on detected gestures.
Volume Control: Utilizes PyCaw to set the system volume level according to hand movements.
# Customization
You can adjust the parameters and thresholds for gesture detection and volume control within the script to fit your specific needs.

# Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

# License
This project is licensed under the MIT License.

