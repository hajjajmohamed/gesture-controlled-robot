#!/usr/bin/env python3
# Gesture Detector - MediaPipe Hand Tracking
# Author: Mohamed Hajjaj - The Inventor Hero
# GitHub: https://github.com/hajjajmohamed

import cv2
import mediapipe as mp
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils

GESTURES = {
    "FORWARD":  "All fingers up",
    "STOP":     "Fist closed",
    "LEFT":     "Point left",
    "RIGHT":    "Point right",
    "BACKWARD": "Thumb down"
}

class GestureDetector(Node):
    def __init__(self):
        super().__init__('gesture_detector')
        self.publisher = self.create_publisher(String, '/gesture/command', 10)
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.cap = cv2.VideoCapture(0)
        self.timer = self.create_timer(0.05, self.process_frame)
        self.get_logger().info('Gesture Detector Node Started')

    def get_finger_states(self, landmarks):
        tips = [4, 8, 12, 16, 20]
        fingers = []
        # Thumb
        fingers.append(1 if landmarks[4].x < landmarks[3].x else 0)
        # Other fingers
        for tip in tips[1:]:
            fingers.append(1 if landmarks[tip].y < landmarks[tip - 2].y else 0)
        return fingers

    def classify_gesture(self, fingers):
        if fingers == [0, 0, 0, 0, 0]:
            return "STOP"
        elif fingers == [1, 1, 1, 1, 1]:
            return "FORWARD"
        elif fingers == [0, 1, 0, 0, 0]:
            return "RIGHT"
        elif fingers == [0, 1, 1, 0, 0]:
            return "LEFT"
        elif fingers == [1, 0, 0, 0, 0]:
            return "BACKWARD"
        return "UNKNOWN"

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        gesture = "UNKNOWN"
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                fingers = self.get_finger_states(hand_landmarks.landmark)
                gesture = self.classify_gesture(fingers)

        color = (0, 255, 0) if gesture != "UNKNOWN" else (0, 0, 255)
        cv2.rectangle(frame, (10, 10), (300, 60), color, -1)
        cv2.putText(frame, f'Gesture: {gesture}',
                    (15, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        cv2.imshow('Gesture Detector - The Inventor Hero', frame)
        cv2.waitKey(1)

        if gesture != "UNKNOWN":
            msg = String()
            msg.data = gesture
            self.publisher.publish(msg)

    def destroy_node(self):
        self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = GestureDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
