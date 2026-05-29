# Gesture-Controlled Robotics System

Control a robot using hand gestures via MediaPipe and computer vision.

## Features
- Real-time hand gesture recognition using MediaPipe
- 5 gesture commands: Forward, Backward, Left, Right, Stop
- ROS2 node architecture
- Live visual overlay with gesture status
- Standalone test mode without ROS2

## Gesture Commands

| Gesture       | Action   |
|---------------|----------|
| All fingers up| FORWARD  |
| Fist closed   | STOP     |
| Index finger  | RIGHT    |
| Two fingers   | LEFT     |
| Thumb down    | BACKWARD |

## Tech Stack

| Category  | Technologies          |
|-----------|-----------------------|
| Vision    | MediaPipe, OpenCV     |
| Framework | ROS2 Humble           |
| Language  | Python 3              |
| Hardware  | Raspberry Pi 4, ESP32 |
| OS        | Ubuntu 22.04          |

## Project Structure

    gesture-controlled-robot/
    src/
        gesture_detector.py    - MediaPipe hand detection node
        robot_controller.py    - Motor control node
        standalone_test.py     - Test without ROS2
    docs/
        wiring.md
    media/
    requirements.txt

## Usage

### Standalone test
    python3 src/standalone_test.py

### Full ROS2 mode
    source /opt/ros/humble/setup.bash
    python3 src/gesture_detector.py
    python3 src/robot_controller.py

## Author
Mohamed Hajjaj - The Inventor Hero
National Innovation Champion 2026
GITEX Africa 2026 Participant
GitHub: https://github.com/hajjajmohamed
Instagram: https://instagram.com/the.inventor.hero
