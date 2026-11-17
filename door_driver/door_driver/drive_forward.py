"""drive_forward: drives the twin straight ahead (its heading at the start) `distance` metres on /odom, then stops."""

import math

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node

from .control import command, progress, wrap, yaw_of


class DriveForward(Node):
    def __init__(self) -> None:
        super().__init__("drive_forward")
        self.distance = float(self.declare_parameter("distance", 2.0).value)
        self.speed = float(self.declare_parameter("speed", 0.4).value)
        self.pub = self.create_publisher(Twist, "cmd_vel", 10)
        self.create_subscription(Odometry, "odom", self.on_odom, 10)
        self.start = None
        self.done = False

    def on_odom(self, msg: Odometry) -> None:
        if self.done:
            return
        p, q = msg.pose.pose.position, msg.pose.pose.orientation
        yaw = yaw_of(q.z, q.w)
        if self.start is None:
            self.start = (p.x, p.y, yaw)
            self.get_logger().info(f"Driving {self.distance:.2f} m forward from ({p.x:.2f}, {p.y:.2f})")
        travelled = progress(self.start, p.x, p.y)
        heading_error = wrap(yaw - self.start[2])
        v, w = command(travelled, self.distance, heading_error, self.speed)
        cmd = Twist()
        cmd.linear.x, cmd.angular.z = v, w
        self.pub.publish(cmd)
        if v == 0.0:
            self.done = True
            self.get_logger().info(
                f"Stopped: {travelled:.3f} m, at ({p.x:.2f}, {p.y:.2f}), heading off by {math.degrees(heading_error):.1f}°")


def main() -> None:
    rclpy.init()
    node = DriveForward()
    try:
        while rclpy.ok() and not node.done:
            rclpy.spin_once(node, timeout_sec=0.1)
        for _ in range(5):  # make sure the stop gets through
            node.pub.publish(Twist())
            rclpy.spin_once(node, timeout_sec=0.05)
    finally:
        node.destroy_node()
        rclpy.shutdown()
