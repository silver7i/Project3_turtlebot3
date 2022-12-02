# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String


class Pub_Griper(Node):

    def __init__(self):
        super().__init__('griper_ctrl_pub')
        qos_profile = QoSProfile(depth=10)
        self.griper_publisher = self.create_publisher(
        	String,
        	'griper_ctrl',
        	qos_profile)
        self.timer = self.create_timer(1, self.pub_ctrl_msg)
        self.count = 0


    def pub_ctrl_msg(self):
        msg = String()
        msg.data = "close"    
        self.griper_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Pub_Griper()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
