#!/usr/bin/env python
#coding: utf-8         # 日本語を使えるようにする

import math
import rospy
import numpy as np
from std_msgs.msg import ColorRGBA
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path

class pathPublisher:
  def __init__( self, topic, cell_size):
    self.cell_size = np.array(cell_size) / 2.0
    self.topic = topic
    self.pub_path = rospy.Publisher( topic, Path, queue_size=10)
    self.path = Path()
    self.path.header.frame_id = "odom"

    self.offset_x = cell_size[0] / -2.0
    self.offset_y = cell_size[1] / -2.0

  def setData( self, path_data):
    poses = [PoseStamped() for i in range(len(path_data))]
    for (i,point) in enumerate(path_data):
      poses[i].header.frame_id = "odom"
      poses[i].pose.position.x = self.cell_size[0] * point[0] + self.offset_x
      poses[i].pose.position.y = self.cell_size[1] * point[1] + self.offset_y
      poses[i].pose.position.z = 0.0
      poses[i].pose.orientation.x = 0.0
      poses[i].pose.orientation.y = 0.0
      poses[i].pose.orientation.z = 0.0
      poses[i].pose.orientation.w = 1.0
    self.path.poses = poses

  def publish( self):
    self.pub_path.publish( self.path)


"""
if __name__=="__main__":
  rospy.init_node("test_node")
  path1 = pathPublisher( "path_red"  , [ 0.200, 0.200])
  path2 = pathPublisher( "path_green", [ 0.200, 0.200])
  path3 = pathPublisher( "path_blue" , [ 0.200, 0.200])
  path1.setData( [[0,0], [1,0], [2,1], [3,0]])
  path2.setData( [[0,0], [0,1], [1,2], [0,3]])
  path3.setData( [[0,0], [1,1], [2,4], [4,2]])
  loop = rospy.Rate(10)
  try:
    while not rospy.is_shutdown():
      path1.publish()
      path2.publish()
      path3.publish()
      loop.sleep()
      pass
  except KeyboardInterrupt:
    print("キーボード割り込み！CTRL-C　終了")
"""
