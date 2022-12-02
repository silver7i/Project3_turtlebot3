
import rclpy, serial
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
ser = serial.Serial('/dev/ttyUSB1', 115200,timeout = 1)

class Sub_Griper(Node):

    def __init__(self):
        super().__init__('griper_ctrl_sub')
        qos_profile = QoSProfile(depth=10)
        self.griper_subscriber = self.create_subscription(
            String,
            'griper_ctrl',
            self.sub_ctrl_msg,
            qos_profile)

    def sub_ctrl_msg(self, msg):
        self.get_logger().info('Received message: {0}'.format(msg.data))
        if msg.data == "close":
        	print("close")
        	ser.write(b'1')
        elif msg.data == "open":
        	print("open")
        	ser.write(b'0')


def main(args=None):
    rclpy.init(args=args)
    node = Sub_Griper()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
