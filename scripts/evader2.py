#!/usr/bin/env python3

import rospy
import random
import tf
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry

vel_pub = rospy.Publisher('/robot_0/cmd_vel', Twist, queue_size=5)
tw = Twist()

def laser_callback(msg):
    
    y = msg.ranges
    y_right = y[0:90]
    y_center = y[91:270]
    y_left = y[271:360]
    #print(y_center)

    front = min(y_center)
    #print("F",front)
    right = min(y_right)
    #print("R",right)
    left = min(y_left)
    #print("L",left)

    ###############################################################

    if front >= 1.5 or (left <1.5 and right <1.5):
        tw.linear.x=2
        tw.angular.z = random.uniform(-7,7)
        vel_pub.publish(tw)
    if left <= 1.5 and (front >= 1.5 or right >=1.5):
        tw.linear.x=1
        tw.angular.z = random.uniform(-7,7)
        vel_pub.publish(tw)
    if right <= 1.5 and (front >= 1.5 or left >=1.5):
        tw.linear.x=1
        tw.angular.z = random.uniform(-7,7)
        vel_pub.publish(tw)
    if front <1:
        tw.linear.x=0
        tw.angular.z = random.uniform(-7,7)
        vel_pub.publish(tw)
    else :
        tw.linear.x=2.0
        tw.angular.z = 0
        vel_pub.publish(tw)

def odom_callback(msg):
    
    xp = msg.pose.pose.position.x
    yp = msg.pose.pose.position.y
    zp = msg.pose.pose.position.z
    xo = msg.pose.pose.orientation.x
    yo = msg.pose.pose.orientation.y
    zo = msg.pose.pose.orientation.z
    wo = msg.pose.pose.orientation.w
    tf.TransformBroadcaster().sendTransform((xp,yp,zp), (xo,yo,zo,wo), rospy.Time.now(), 'robot_0', 'world')


def evader() :
    rospy.init_node('evader', anonymous=True)
    laser_sub = rospy.Subscriber('/robot_0/base_scan', LaserScan, laser_callback)
    odom_sub = rospy.Subscriber('/robot_0/base_pose_ground_truth', Odometry, odom_callback)
    rospy.spin()
	

if __name__ == '__main__':
	evader()
		
		
	
