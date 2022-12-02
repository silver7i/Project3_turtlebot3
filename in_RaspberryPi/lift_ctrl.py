from select import select
import serial
import os, time, sys, termios, atexit, tty

class GetChar:
    def __init__(self):
        # Save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)
  
        # New terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
  
        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)      
      
    def set_normal_term(self):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)
  
    def getch(self):        # get 1 byte from stdin
        """ Returns a keyboard character after getch() has been called """
        return sys.stdin.read(1)
  
    def chk_stdin(self):    # check keyboard input
        """ Returns True if keyboard character was hit, False otherwise. """
        dr, dw, de = select([sys.stdin], [], [], 0)
        return dr


if __name__ == '__main__':

    try:
        sp  = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        kb  = GetChar()
        dat = ""
        
        while True:
            
            ch = kb.getch()
            
            if   ch == '1':
                sp.write(b'1')                
                
            elif ch == '0':
                sp.write(b'0')                
                
            elif ch == 'q':
                sp.write(b'q')
            
            else:
                pass
            
    except KeyboardInterrupt:
        pass
'''               
class LiftCtrl(Node):
    
    def __init__(self):
        super().__init__('lift_ctrl')
        qos_profile = QoSProfile(depth=10)
        self.sub_ctrl_msg = self.create_subscription(
            String,
            'lift_ctrl_msg',
            self.get_ctrl_msg,
            qos_profile)
            
    
        if sp.readable():
            rcv = sp.readline()
            rcv = (rcv.decode()[:len(rcv) - 1])
                
            
    def get_ctrl_msg(self, msg):
        
        data = ""
        
        if   msg.data == "lift_up":
            sp.write(b'1');  print("lift up")
            
            while data != "stop":
                if sp.readable():
                    data = (rcv.decode()[:len(rcv) - 1])
        
        elif msg.data == "lift_down":
            sp.write(b'0');  print("lift down")
            
            while data != "stop":
                if sp.readable():
                    data = (rcv.decode()[:len(rcv) - 1])
        
        else:   pass
           
        
def main(args=None):
    rclpy.init(args=args)
    node = LiftCtrl()
    
    try:
        rclpy.spin(node)
                
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt(SIGINT)')
        
    finally:
        node.destroy_node()
        rclpy.shutdown()
    
            
if __name__ == '__main__':
    main()
'''
