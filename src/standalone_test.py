#!/usr/bin/env python3
# Standalone Gesture Test - No ROS2 needed
# Author: Mohamed Hajjaj - The Inventor Hero

import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils

def get_finger_states(landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []
    fingers.append(1 if landmarks[4].x < landmarks[3].x else 0)
    for tip in tips[1:]:
        fingers.append(1 if landmarks[tip].y < landmarks[tip - 2].y else 0)
    return fingers

def classify_gesture(fingers):
    if fingers == [0, 0, 0, 0, 0]: return "STOP"
    if fingers == [1, 1, 1, 1, 1]: return "FORWARD"
    if fingers == [0, 1, 0, 0, 0]: return "RIGHT"
    if fingers == [0, 1, 1, 0, 0]: return "LEFT"
    if fingers == [1, 0, 0, 0, 0]: return "BACKWARD"
    return "UNKNOWN"

cap = cv2.VideoCapture(0)
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
print("Gesture Test - The Inventor Hero | Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    gesture = "UNKNOWN"

    if results.multi_hand_landmarks:
        for lm in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
            gesture = classify_gesture(get_finger_states(lm.landmark))

    color = (0, 255, 0) if gesture != "UNKNOWN" else (0, 0, 255)
    cv2.rectangle(frame, (10, 10), (300, 60), color, -1)
    cv2.putText(frame, f'Gesture: {gesture}',
                (15, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
    cv2.imshow('Gesture Test', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
