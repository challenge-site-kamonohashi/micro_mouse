#!/usr/bin/env python
#coding: utf-8         # 日本語を使えるようにする

import roslib.packages
pk_path = roslib.packages.get_pkg_dir('micro_mouse')
import sys
sys.path.append(pk_path + '/script/lib')

import math
import numpy as np
import rospy  # include<ros/ros.h>のようなもの

import heatmap


if __name__ == '__main__': # int main()みたいな
  rospy.init_node("node_name") # ノード設定

  cell_matrix = [ 10, 10]
  cell_size = [ 0.200, 0.200]
  heatmap = heatmap.heatmapPublisher("heatmap_red", cell_matrix, cell_size)
  map_data = np.arange(100).reshape(10,10)

  try:
    loop = rospy.Rate(10) # 10[loop/s]の設定をする。
    while not rospy.is_shutdown():
#-----ここにプログラムを書く-----
      heatmap.setData( map_data, heatmap.RED, 100)
  #-----地図情報を表示する-----
      heatmap.publish()
#-----ここまで-----
      loop.sleep() # 10[loop/s]になるよう調整する。
  except KeyboardInterrupt: # try:中にCTRL-Cが押されればココを実行する。
    print("キーボード割り込み！CTRL-C　終了")
