#!/usr/bin/env python
#coding: utf-8         # 日本語を使えるようにする

import roslib.packages
pk_path = roslib.packages.get_pkg_dir('micro_mouse')
import sys
sys.path.append(pk_path + '/script/lib')

import rospy  # include<ros/ros.h>のようなもの

import path


if __name__=="__main__":
  rospy.init_node("node_name")
  path1 = path.pathPublisher( "path_red"  , [ 0.200, 0.200])
  path2 = path.pathPublisher( "path_green", [ 0.200, 0.200])
  path3 = path.pathPublisher( "path_blue" , [ 0.200, 0.200])
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
