#!/usr/bin/env python3
# Robot Controller - Reacts to gesture commands
# Author: Mohamed Hajjaj - The Inventor Hero

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String

SPEED_LINEAR  = 0.3
SPEED_ANGULAR = 0.5

class GestureRobotController(Node):
    def __init__(self):
        super().__init__('gesture_robot_controller')
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.create_subscription(String, '/gesture/command', self.gesture_callback, 10)
        self.get_logger().info('Gesture Robot Controller Started')

    def gesture_callback(self, msg):
        gesture = msg.data
        twist = Twist()

        if gesture == "FORWARD":
            twist.linear.x = SPEED_LINEAR
            self.get_logger().info('Moving FORWARD')

        elif gesture == "BACKWARD":
            twist.linear.x = -SPEED_LINEAR
            self.get_logger().info('Moving BACKWARD')

        elif gesture == "LEFT":
            twist.angular.z = SPEED_ANGULAR
            self.get_logger().info('Turning LEFT')

        elif gesture == "RIGHT":
            twist.angular.z = -SPEED_ANGULAR
            self.get_logger().info('Turning RIGHT')

        elif gesture == "STOP":
            self.get_logger().warn('STOP gesture - Halting')

        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = GestureRobotController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.cmd_pub.publish(Twist())
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
