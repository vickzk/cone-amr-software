"""drive_aisle: drives the twin straight ahead (its heading at the start) for `distance` metres on /odom, then stops."""

import math

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node

from .control import command, wrap, yaw_of


class DriveAisle(Node):
    def __init__(self) -> None:
        super().__init__("drive_aisle")
        self.distance = float(self.declare_parameter("distance", 8.0).value)
        self.speed = float(self.declare_parameter("speed", 0.5).value)
        self.pub = self.create_publisher(Twist, "cmd_vel", 10)
        self.create_subscription(Odometry, "odom", self.on_odom, 10)
        self.start = None
        self.done = False

    def on_odom(self, msg: Odometry) -> None:
        p, q = msg.pose.pose.position, msg.pose.pose.orientation
        yaw = yaw_of(q.z, q.w)
        if self.start is None:
            self.start = (p.x, p.y, yaw)
            self.get_logger().info(f"Driving {self.distance:.1f} m from ({p.x:.2f}, {p.y:.2f})")
        x0, y0, yaw0 = self.start
        travelled = math.hypot(p.x - x0, p.y - y0)
        v, w = command(travelled, self.distance, wrap(yaw - yaw0), self.speed)
        cmd = Twist()
        cmd.linear.x, cmd.angular.z = v, w
        self.pub.publish(cmd)
        if v == 0.0 and not self.done:
            self.done = True
            self.get_logger().info(f"Arrived: {travelled:.2f} m, heading off by {math.degrees(wrap(yaw - yaw0)):.1f}°")


def main() -> None:
    rclpy.init()
    node = DriveAisle()
    try:
        while rclpy.ok() and not node.done:
            rclpy.spin_once(node, timeout_sec=0.1)
        node.pub.publish(Twist())
    finally:
        node.destroy_node()
        rclpy.shutdown()
