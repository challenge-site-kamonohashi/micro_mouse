#!/usr/bin/env python
#coding: utf-8         # 日本語を使えるようにする

#-----include ros libraries-----
import roslib.packages
import sys
pk_path = roslib.packages.get_pkg_dir('micro_mouse')
sys.path.append(pk_path + '/script/lib')
import rospy
import mouse
import heatmap
import path
import pathplanning
import wall
#-----include std libraries-----
import math
#-----include extends libraries
import numpy as np


if __name__ == '__main__': # int main()みたいな
  rospy.init_node("node_name") # ノード設定
#-----object等の定義-----
  cell_matrix = [ 17, 17]
  cell_size = [ 0.200, 0.200]
  mouse = mouse.Mouse()
  walls = wall.wallPublisher("wall_marker", cell_matrix, cell_size)
  path  = path.pathPublisher( "path_red"  , cell_size)
#-----User定義変数-----
  a = 0
  b = 3
  c = 5


  try:
    loop = rospy.Rate(10) # 10[loop/s]の設定をする。
    while not rospy.is_shutdown():
#-----ここにプログラムを書く-----
#-----ここまで-----
      loop.sleep() # 10[loop/s]になるよう調整する。
  except KeyboardInterrupt: # try:中にCTRL-Cが押されればココを実行する。
    print("キーボード割り込み！CTRL-C　終了")
