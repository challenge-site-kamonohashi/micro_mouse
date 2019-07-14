#!/usr/bin/env python
#coding: utf-8         # 日本語を使えるようにする

import math
import numpy as np
import rospy  # include<ros/ros.h>のようなもの
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

import wall


class LightSensor:
  def __init__( self, topic):
    rospy.Subscriber( topic, Float32, self.callbackLight)
    self.data = 0

  def callbackLight( self, light):
    self.data = light.data
    

class Mouse:
  def __init__( self, topic_drive, topics_sensor):
    print("hello_mouse!")
    self.pub_twist = rospy.Publisher( topic_drive, Twist, queue_size=10)
    self.sensor = [ None for i in range(len(topics_sensor))]
    for (i,topic) in enumerate(topics_sensor):
      self.sensor[ i] = LightSensor( topic)

    self.move(0.0, 0.0, 5)

  def move( self, fwd, ang, cnt=10):
    msg = Twist()
    msg.linear.x = fwd
    msg.angular.z = ang
  
    loop = rospy.Rate(10)
    for i in range(cnt):
      self.pub_twist.publish( msg)
      loop.sleep()
