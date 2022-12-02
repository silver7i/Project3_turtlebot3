import rclpy, serial
from rclpy.node import Node

from std_msgs.msg import String

sp  = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)

class PubLED_MSG(Node):

    def __init__(self):
        self.goal=''
        super().__init__('pub_goal_msg')
        self.pub = self.create_publisher(String, 'goal_msg', 10)
        self.led_msg = String()
        
    def pub_goal_msg(self, goal_msg):
        msg = String()
        msg.data = goal_msg
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    node = PubLED_MSG()
    
    #rclpy.spin(node)
    try:
        while rclpy.ok():
            rcv = sp.read().decode('ascii')
            if rcv == 'a':
                print("mang")
                node.pub_goal_msg('1')
            elif rcv == 'b':
                print("silver")
                node.pub_goal_msg('2')
            elif rcv == 'c':
            	print("dong")
            	node.pub_goal_msg('3')
            else:
                pass
    except KeyboardInterrupt:
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    
            node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()
