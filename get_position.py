#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import csv
from geometry_msgs.msg import PoseStamped
from tf.transformations import euler_from_quaternion


#Turtlebot
class Turtlebot():
    def __init__(self, name):
        self.turtlebot = name
        self.file = self.turtlebot +'.csv'
        rospy.init_node(self.turtlebot+'control', anonymous=False)

        #get it's pos and orientation
        self.pose_subscriber = rospy.Subscriber("/vrpn_client_node/"+self.turtlebot+'/pose', PoseStamped, self.pose_callback)
        self.state = [0, 0, 0] #x, y, z
        
    def pose_callback(self,data):
        """Callback function which is called when a new message of type Pose is received by the subscriber."""
        self.position = data.pose.position
        euler_angles = euler_from_quaternion( quaternion=( data.pose.orientation.x,data.pose.orientation.y, data.pose.orientation.z,data.pose.orientation.w))
        self.theta = euler_angles[2]
        # get x, y, z
        self.state = [data.pose.position.x, data.pose.position.y, data.pose.position.z]
    
    def save_pos(self):
       with open(self.file, "w+") as file:
           csv_file = csv.writer(file)
           while not rospy.is_shutdown():
               csv_file.writerow(self.state)
               print(self.state)

    @staticmethod
    def main():
        rospy.spin()


if __name__ == '__main__':
    rigid_name = "robot1"
    k = Turtlebot(rigid_name)
    k.save_pos()
    rospy.spin()

