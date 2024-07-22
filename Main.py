import cv2
import mediapipe as mp
import math
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from time import sleep

def set_volume_percentage(volume_percentage):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume_range = volume.GetVolumeRange()
    min_vol_db, max_vol_db, _ = volume_range

    # Calculate volume level from percentage
    volume_level = int((max_vol_db - min_vol_db) * (volume_percentage / 100.0) + min_vol_db)
    volume.SetMasterVolumeLevel(volume_level, None)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.1, min_tracking_confidence=0.9)
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def little_finger_up(landmarks):
    global little_finger_pip
    """ Check if the little finger is upright. """
    little_finger_tip = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    little_finger_pip = landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
    return little_finger_tip.y < little_finger_pip.y

# Get the screen size
screen_width, screen_height = pyautogui.size()

clicking = False
volume_min_y = 400
volume_max_y = 1400
initial_x = None
initial_y = None
x_positions = []
y_positions = []

def smooth_movement(positions, window_size=5):
    if len(positions) < window_size:
        return positions[-1]
    return sum(positions[-window_size:]) / window_size

y_threshold = 30  # Buffer for y-axis

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)
    
    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame to detect hands
    result = hands.process(rgb_frame)
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw hand landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            h, w, _ = frame.shape
            
            # Get the positions of the thumb, index, and middle finger tips
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            little_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            little_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            middle_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
            
            thumb_tip_pos = (int(thumb_tip.x * w), int(thumb_tip.y * h))
            index_finger_tip_pos = (int(index_finger_tip.x * w), int(index_finger_tip.y * h))
            middle_finger_tip_pos = (int(middle_finger_tip.x * w), int(middle_finger_tip.y * h))
            little_finger_tip_pos = (int(little_finger_tip.x * w), int(little_finger_tip.y * h))
            wrist_pos = (int(wrist.x * w), int(wrist.y * h))
            middle_finger_mcp_pos = (int(middle_finger_mcp.x * w), int(middle_finger_mcp.y * h))
            
            # Draw circles at the finger tips
            cv2.circle(frame, thumb_tip_pos, 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, index_finger_tip_pos, 10, (0, 255, 0), cv2.FILLED)
            cv2.circle(frame, middle_finger_tip_pos, 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, little_finger_tip_pos, 10, (255, 255, 0), cv2.FILLED)
            
            # Move the mouse cursor to the middle finger tip position if it's the right hand
            if wrist_pos[0] > middle_finger_mcp_pos[0]:  # Compare x-coordinates of wrist and middle finger MCP
                screen_x = int(middle_finger_tip.x * screen_width)
                screen_y = int(middle_finger_tip.y * screen_height)
                
                # Check if the hand is upright and the little finger is up
                if wrist_pos[1] > middle_finger_mcp_pos[1] and little_finger_up(hand_landmarks):
                    # Check the distance between the thumb and index finger tips
                    distance = calculate_distance(thumb_tip_pos, index_finger_tip_pos)
                    distance_middle = calculate_distance(thumb_tip_pos, middle_finger_tip_pos)
                  #  distance_little =calculate_distance(little_finger_pip, little_finger_tip_pos)
                    if distance_middle < 30: #fixxx this and here sidatnce ofr lillte:
                        pyautogui.press("playpause")
                        print("Playpause")
                        sleep(0.2)
                    if distance < 25:  # Reduced threshold for more precise touch detection
                        if not clicking:
                            clicking = True
                            initial_x = thumb_tip_pos[0]
                            initial_y = thumb_tip_pos[1]
                            x_positions.clear()
                            y_positions.clear()
                            cv2.putText(frame, "Click and Drag!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
                        else:
                            x_positions.append(thumb_tip_pos[0])
                            y_positions.append(thumb_tip_pos[1])
                            smooth_x = smooth_movement(x_positions)
                            smooth_y = smooth_movement(y_positions)
                            if initial_x is not None and initial_y is not None:
                                if abs(smooth_y - initial_y) < y_threshold:  # Ensure y-axis is stable
                                    if smooth_x - initial_x > 30:
                                        pyautogui.press("nexttrack")
                                        print("Next track")
                                        initial_x = None
                                        initial_y = None
                                        x_positions.clear()
                                        y_positions.clear()
                                    elif initial_x - smooth_x > 30:
                                        pyautogui.press("prevtrack")
                                        print("Previous track")
                                        initial_x = None
                                        initial_y = None
                                        x_positions.clear()
                                        y_positions.clear()
                    else:
                        if clicking:
                            clicking = False
                            initial_x = None
                            initial_y = None
                            x_positions.clear()
                            y_positions.clear()
                            
                    # Calculate the percentage volume based on screen Y coordinate
                    if screen_y >= volume_min_y and screen_y <= volume_max_y and clicking:
                        percentage_volume = (screen_y - volume_min_y) / (volume_max_y - volume_min_y) * 100.0
                        set_volume_percentage((100 - int(percentage_volume)))
                        print((100 - int(percentage_volume)))
    
    # Display the frame
    cv2.imshow('Hand Tracking', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
      
