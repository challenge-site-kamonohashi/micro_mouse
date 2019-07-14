#!/usr/bin/env python
#coding: utf-8

import math
import rospy
from std_msgs.msg import Float32
from sensor_msgs.msg import LaserScan

class ScanToLight:
  def __init__( self, rang):
    self.range = rang
    rospy.Subscriber("base_scan", LaserScan, self.callbackLaserScan)
    self.pub_light = [ rospy.Publisher("scan/R", Float32, queue_size=10),
                       rospy.Publisher("scan/FR", Float32, queue_size=10),
                       rospy.Publisher("scan/F", Float32, queue_size=10),
                       rospy.Publisher("scan/FL", Float32, queue_size=10),
                       rospy.Publisher("scan/L", Float32, queue_size=10)]
    self.angles = []
    self.setLightAngle( [ -math.pi/2, -math.pi/4,  0,  math.pi/4,  math.pi/2])
    
  def setLightAngle( self, angles):
    self.angles = angles
    self.strength = [ 0 for i in range(len( angles))]
    
  def callbackLaserScan( self, laser):
    for (i,angle) in enumerate(self.angles):
      num = int((angle - laser.angle_min) / laser.angle_increment)
      self.pub_light[ i].publish( Float32( laser.ranges[ num]))


if __name__ == '__main__':
  rospy.init_node("scan_to_light")
  trans = ScanToLight( 0)
  rospy.spin()
