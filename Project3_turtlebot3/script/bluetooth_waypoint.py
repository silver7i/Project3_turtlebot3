import time
import os,sys
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped 
from rclpy.action import ActionClient
from action_msgs.msg import GoalStatus
from nav2_msgs.action import FollowWaypoints
from std_msgs.msg import String
# from rclpy.duration import Duration # Handles time for ROS 2


class ClientFollowPoints(Node):
    def __init__(self):
    	self.goal_now = ''
    	self.goal_prv = ''
    	self.goal_changed = False
    	super().__init__('client_follow_points')
    	self.subscription = self.create_subscription(
    		String, 'goal_msg', self.get_goal_msg, 10 )
    	self._client = ActionClient(self, FollowWaypoints, '/FollowWaypoints')
    def get_goal_msg(self, msg):
    	self.goal_now = msg.data
    	if self.goal_now != self.goal_prv:
    		self.goal_prv = self.goal_now
    		self.goal_changed = True
    	print(self.goal_now)

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
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
        	self.get_logger().info('succeeded!')
        	self.get_logger().info('succeeded(all formula): {0}'.format(result.all_formula))
        	self.get_logger().info('succeeded(total sum): {0}'.format(result.total_sum))
        self.get_logger().info('Result: {0}'.format(result.missed_waypoints))

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.current_waypoint))
'''    def spin(node: 'Node', executor: 'Executor' =None) -> None:
        executor = get_global_executor() if executor is None else executor
        try:
        	executor.add_node(node)
        	while executor.context.ok():
        		executor.spin_once()
        finally:
        	executor.remove(node)
'''	
	
def main(args=None):
    rclpy.init(args=args)

    client = ClientFollowPoints()
    print('client inited')

    goal0 = PoseStamped()
    goal0.header.frame_id = "map"
    goal0.header.stamp.sec = 0
    goal0.header.stamp.nanosec = 0
    goal0.pose.position.z = 0.0
    goal0.pose.position.x = 0.971
    goal0.pose.position.y = 1.84
    goal0.pose.orientation.w = 1.0
    
    goal1 = PoseStamped()
    goal1.header.frame_id = "map"
    goal1.header.stamp.sec = 0
    goal1.header.stamp.nanosec = 0
    goal1.pose.position.z = 0.0
    goal1.pose.position.x = 0.493
    goal1.pose.position.y = -0.0109
    goal1.pose.orientation.w = 1.0
    
    goal2 = PoseStamped()
    goal2.header.frame_id = "map"
    goal2.header.stamp.sec = 0
    goal2.header.stamp.nanosec = 0
    goal2.pose.position.z = 0.0
    goal2.pose.position.x = 0.141
    goal2.pose.position.y = 0.0426
    goal2.pose.orientation.w = 1.0    
    try:    
        while rclpy.ok():
            rclpy.spin_once(client)
            if client.goal_changed is True:
                if client.goal_now == '1':
                    mgoal = [goal0]                   
                    client.send_points(mgoal)
                    client.goal_now = 0
                    dong = 1
                    
                elif client.goal_now == '2':
                    mgoal = [goal1]
                    client.send_points(mgoal)
                    client.goal_now = 0
                    dong = 2
                elif client.goal_now == '3':
                    mgoal = [goal2]
                    client.send_points(mgoal)
                    client.goal_now = 0
                    dong = 3
                
                    
                  
    #print(rgoal)
    #mgoal = [rgoal]

#        client.send_points(mgoal)

    #rclpy.spin(client)
                
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt(SIGINT)')
        
    finally:
        client.destroy_node()
        if dong == 1:
             os.system("ros2 run ar_track track_marker5 7")

                    
        elif dong == 2:
             os.system("ros2 run ar_track track_marker5 8")

        elif dong == 3:
             os.system("ros2 run ar_track track_marker5 9")


        rclpy.shutdown()
    
