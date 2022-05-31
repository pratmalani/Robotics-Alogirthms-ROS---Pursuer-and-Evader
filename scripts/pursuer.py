#!/usr/bin/env python3

from curses import REPORT_MOUSE_POSITION
from gettext import translation
import rospy
import tf
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

def odom_callback(msg) :
	xp = msg.pose.pose.position.x
	yp = msg.pose.pose.position.y
	zp = msg.pose.pose.position.z
	xo = msg.pose.pose.orientation.x
	yo = msg.pose.pose.orientation.y
	zo = msg.pose.pose.orientation.z
	wo = msg.pose.pose.orientation.w
	tf.TransformBroadcaster().sendTransform((xp,yp,zp), (xo,yo,zo,wo), rospy.Time.now(), '/robot_1', '/world')

def pursuer() :
	rospy.init_node('pursuer', anonymous=True)
	vel_pub = rospy.Publisher('/robot_1/cmd_vel', Twist, queue_size=5)
	odom_listener = rospy.Subscriber('/robot_1/base_pose_ground_truth', Odometry, odom_callback)
	tw = Twist()
		
	rate = rospy.Rate(15)
	listener = tf.TransformListener()
	while not rospy.is_shutdown() :
		try:
			translation, orientation= listener.lookupTransform('robot_1', 'robot_0', rospy.Time.now())
		except:
			continue

		
		xe, ye, ze = translation
		tw.linear.x = 0.5 * math.sqrt(pow(xe, 2) + math.pow(ye, 2))
		tw.angular.z = 1 * math.atan2(ye, xe)
		vel_pub.publish(tw) 			
		   	
	rospy.spin()

if __name__ == '__main__':
	pursuer()
