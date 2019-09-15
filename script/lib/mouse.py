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
  def __init__( self, control_topic="cmd_vel", sensors_topic=["scan/R","scan/FR","scan/F","scan/FL","scan/L"], sensor_rad=[-math.pi/2, math.pi/4,     0, math.pi/4, math.pi/2]):
    self.control_topic = control_topic
    self.sensors_topic = sensors_topic
    self.sensor_rad = sensor_rad
    print("hello_mouse!")
    self.pub_twist = rospy.Publisher( control_topic, Twist, queue_size=10)
    self.sensor = [ LightSensor(topic) for topic in sensors_topic]

    self.move(0.0, 0.0, 5)

  def move( self, fwd, ang, cnt=10):
    msg = Twist()
    msg.linear.x = fwd
    msg.angular.z = ang
  
    loop = rospy.Rate(10)
    for i in range(cnt):
      self.pub_twist.publish( msg)
      loop.sleep()

  def getSensor( self):
    return np.array([ sensor.data for sensor in self.sensor])
