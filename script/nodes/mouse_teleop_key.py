#!/usr/bin/env python
#coding: utf-8

import math
import rospy
from geometry_msgs.msg import Twist
from getch import getch, pause


def move( fwd, ang):
  loop = rospy.Rate(5)
  msg = Twist()
  msg.linear.x = fwd
  msg.angular.z = ang
  pub_twist = rospy.Publisher( "cmd_vel", Twist, queue_size=10)

  for i in range(5):
    pub_twist.publish( msg)
    loop.sleep()


if __name__ == '__main__':
  rospy.init_node("mouse_teleop")
  move(0.0, 0.0)

  print('move by "w,a,s,d"  exit by "k"')
  loop = rospy.Rate(10)
  while not rospy.is_shutdown():
    key = getch()
    if key == 'w':
      move( 1.0, 0.0)
    elif key == 's':
      move(-1.0, 0.0)
    elif key == 'a':
      move( 0.0, math.pi/2)
    elif key == 'd':
      move( 0.0,-math.pi/2)
    elif key == 'k':
      print("")
      break
    loop.sleep()
