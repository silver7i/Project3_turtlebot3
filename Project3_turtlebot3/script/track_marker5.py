import rclpy, os, sys
#from follow_waypoints_ter import ClientFollowPoints # 추가
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from geometry_msgs.msg import Pose, Twist
from ros2_aruco_interfaces.msg import ArucoMarkers
from math import degrees, radians, sqrt, sin, cos, pi
from tf_transformations import euler_from_quaternion #, quaternion_from_euler
from ar_track.move_tb3 import MoveTB3
from geometry_msgs.msg import PoseStamped 
from nav_msgs.msg import Odometry
import time
from geometry_msgs.msg import PoseStamped 
from rclpy.action import ActionClient
from action_msgs.msg import GoalStatus
from nav2_msgs.action import FollowWaypoints


TARGET_ID = int(sys.argv[1]) # argv[1] = id of target marker

# Turtlebot3 Specification
MAX_LIN_SPEED =  0.22
MAX_ANG_SPEED =  2.84


# make default speed of linear & angular
LIN_SPEED = MAX_LIN_SPEED * 0.075
ANG_SPEED = MAX_ANG_SPEED * 0.075

R = 1.5708

class ClientFollowPoints(Node):

    def __init__(self):
        super().__init__('client_follow_points')
        self._client = ActionClient(self, FollowWaypoints, '/FollowWaypoints')

    def send_points(self, points):
        msg = FollowWaypoints.Goal()
        msg.poses = points

        self._client.wait_for_server()
        self._send_goal_future = self._client.send_goal_async(msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.missed_waypoints))

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.current_waypoint))

class TrackMarker(Node):
    """   
                                                    ////////////| ar_marker |////////////
            y                      z                --------+---------+---------+--------
            ^  x                   ^                        |     R-0/|\R-0    R|
            | /                    |                        |       /0|0\       |
     marker |/                     | robot                  |      /  |  \      |
            +------> z    x <------+                        |     /   |   \     |
                                  /                         |  dist   |  dist   |
                                 /                          |   /     |     \   |
                                y                           |  /      |      \  |
                                                            | /       |       \0|
                                                            |/R-0    R|R    R-0\|
    pose.x = position.z                             (0 < O) x---------+---------x (0 > O)
    pose.y = position.x              [0]roll    (pos.x > O) ^                   ^ (pos.x < O)
    theta  = euler_from_quaternion(q)[1]pitch*              |                   |            
                                     [2]yaw               robot               robot
    """   
    def __init__(self):
        
        super().__init__('track_marker')
        qos_profile = QoSProfile(depth=10)
        
        self.sub_ar_pose  = self.create_subscription(
            ArucoMarkers,           # topic type
            'aruco_markers',        # topic name
            self.get_marker_pose_,  # callback function
            qos_profile)
            
        self.pub_tw   = self.create_publisher(Twist, '/cmd_vel', qos_profile)
        self.pub_griper = self.create_publisher(String, 'griper_ctrl', qos_profile)
        self.timer    = self.create_timer(1, self.count_sec)
        
        self.pose = Pose()
        self.tw   = Twist()
        self.tb3  = MoveTB3()
        self.griper = String()
        
        self.theta   = 0.0
        self.dir     = 0
        self.th_ref  = 0.0
        self.z_ref   = 0.0
        self.cnt_sec = 0
        
        self.target_found = False
        
        
    def get_marker_pose_(self, msg):
        """
        orientation x,y,z,w ----+
                                +--4---> +-------------------------+
        input orientaion of marker-----> |                         |
                                         | euler_from_quaternion() |
        returnned rpy of marker <------- |                         |
                                +--3---- +-------------------------+
        r,p,y angle <-----------+
                                         +------------+------------+
                                         |   marker   |   robot    |
                                         +------------+------------+
          r: euler_from_quaternion(q)[0] | roll   (x) | (y) pitch  |
        * p: euler_from_quaternion(q)[1] | pitch  (y) | (z) yaw ** | <-- 
          y: euler_from_quaternion(q)[2] | yaw    (z) | (x) roll   | 
                                         +------------+------------+
        """
        if len(msg.marker_ids) == 0:    # no marker found
            self.target_found = False
        
        else: # if len(msg.marker_ids) != 0: # marker found at least 1EA
        
            for i in range(len(msg.marker_ids)):
            
                if msg.marker_ids[i] == TARGET_ID:  # target marker found
                    if self.target_found == False:
                        self.target_found = True                        
                    self.pose  = msg.poses[i]
                    self.theta = self.get_theta(self.pose)
                else:
                    self.target_found = False            
        
    def get_theta(self, msg):
        q = (msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w)
        euler = euler_from_quaternion(q)
        theta = euler[1]        
        return theta
    
    def count_sec(self):
        self.cnt_sec = self.cnt_sec + 1    
        
    def pub_griper_ctrl(self, ctrl_msg):
        self.griper.data = ctrl_msg
        self.pub_griper.publish(self.griper)
    
    def stop_move(self):
        self.tw.linear.z = self.tw.angular.z = 0.0
        self.pub_tw.publish(self.tw)
        
    def publish_griper_ctrl(self, ctrl_msg):
        msg = String()
        msg = ctrl_msg
        self.pub_ctrl.publish(msg)        


        
def main(args=None):
	pose = Pose()
	rclpy.init(args=args)
	node = TrackMarker()
	node.tw.angular.z = 1.5 * ANG_SPEED
	rgoal = PoseStamped()
	rgoal.header.frame_id = "map"
	rgoal.header.stamp.sec = 0
	rgoal.header.stamp.nanosec = 0
	follow_points_client = ClientFollowPoints() # 추가
	
	try:    
		while rclpy.ok():
			if node.theta != 0.0:   break   # this means target marker found
			node.pub_tw.publish(node.tw)
			rclpy.spin_once(node, timeout_sec=0.1)
			
		node.stop_move()
		print("\n----- 1_target marker found!\n") ###########################
		
		while node.pose.position.x < -0.0155 or node.pose.position.x >  0.0155:
		
			if  node.pose.position.x < -0.0155:
				node.tw.angular.z =  0.125 * ANG_SPEED
			else:# node.pose.position.x >  0.025:
				node.tw.angular.z = -0.125 * ANG_SPEED
			node.pub_tw.publish(node.tw)
			rclpy.spin_once(node, timeout_sec=0.1)
			
		node.pub_griper_ctrl("open")
		print("\n----- griper open!\n") ####################
		
		node.stop_move()
		print("\n----- 2_arrived reference position!\n") ####################
		
		node.th_ref = node.theta      # 다시 추가
		node.z_ref  = node.pose.position.z
		if node.th_ref >= 0:
			node.dir =  1
		else:
			node.dir = -1
			
		angle = R - node.th_ref
		
		if angle > R:
			angle = pi - angle
			
		if   node.th_ref > radians( 10):
			node.tb3.rotate( angle * .9)
		elif node.th_ref < radians(-10):
			node.tb3.rotate(-angle * .97)
		else:
			pass
		print("\n----- 3_1st rotation finished!\n") #########################
		
		dist1 = abs(node.z_ref * sin(node.th_ref) * 1.125)
		node.tb3.straight(dist1)
		print("\n----- 4_move to front of marker end!\n") ###################
		
		if   node.th_ref >  radians(10):
			node.tb3.rotate(-R * 0.875)
		elif node.th_ref < -radians(10):
			node.tb3.rotate( R)
		else:
			pass
		print("\n----- 5_2nd rotation finished!\n") #########################
		
		while node.pose.position.x < -0.0025 or node.pose.position.x >  0.0025:
			if   node.pose.position.x < -0.0025:
				node.tw.angular.z =  0.075 * ANG_SPEED
			elif node.pose.position.x >  0.0025:
				node.tw.angular.z = -0.075 * ANG_SPEED
			else:
				node.tw.angular.z =  0.0
				
			node.pub_tw.publish(node.tw)
			rclpy.spin_once(node, timeout_sec=0.02)
			
			
			
			#print(node.pose)
		
		
		
		dist2 = node.pose.position.z - 0.185
		node.tb3.straight(dist2)
		print("\n----- 6_arrived griper position!\n") ####################
		
		node.pub_griper_ctrl("close")
		duration = node.cnt_sec + 3
		
		
		while node.cnt_sec < duration:
			print(duration - node.cnt_sec)
			rclpy.spin_once(node, timeout_sec=1.0)
		print("\n----- 7_finished loading!\n") ############################

		if TARGET_ID==7 or TARGET_ID==8 :
			node.tb3.straight(-dist2)
			node.tb3.rotate(R * node.dir)
			node.tb3.straight(-dist1)
		else :
			node.tb3.straight(-0.1)
		
		print("\n----- 8_finished!\n") ############################
		
		
		while 1: 
			rgoal.pose.position.z = 0.0
			rgoal.pose.position.x = 0.23
			rgoal.pose.position.y = 1.15
		
			print(rgoal)
			mgoal = [rgoal]
			print('goend')
			follow_points_client.send_points(mgoal) # 좌표값 전송

			print("mgoal\n") ##############################
			
			if TARGET_ID==7:
				duration = node.cnt_sec + 35
				while node.cnt_sec < duration:
					print(duration - node.cnt_sec)
					rclpy.spin_once(node, timeout_sec=1.0)
			elif TARGET_ID==8:
				duration = node.cnt_sec + 35
				while node.cnt_sec < duration:
					print(duration - node.cnt_sec)
					rclpy.spin_once(node, timeout_sec=1.0)
			elif TARGET_ID==9:
				duration = node.cnt_sec + 55
				while node.cnt_sec < duration:
					print(duration - node.cnt_sec)
					rclpy.spin_once(node, timeout_sec=1.0)
			rgoal.pose.orientation.w = 1.0
			node.pub_griper_ctrl("open")	
			
			node.tb3.straight(-0.07)
			print("\n----- 9_back!\n") ############################	
			node.pub_griper_ctrl("close")
				
				
			print("success!\n")
			break
			
		sys.exit(1)
		rclpy.spin(node)
		
	except KeyboardInterrupt:
		node.get_logger().info('Keyboard Interrupt(SIGINT)')
		
	finally:
		node.destroy_node()
		os.system("ros2 run ar_track bluetooth_waypoint")
		rclpy.shutdown()			

if __name__ == '__main__':
	main()
    
