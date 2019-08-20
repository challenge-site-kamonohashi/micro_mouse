#!/usr/bin/env python
#coding: utf-8         # 日本語を使えるようにする

import roslib.packages
pk_path = roslib.packages.get_pkg_dir('micro_mouse')
import sys
sys.path.append(pk_path + '/script/lib')

import math
import numpy as np
import rospy  # include<ros/ros.h>のようなもの

import wall


if __name__ == '__main__': # int main()みたいな
  rospy.init_node("node_name") # ノード設定

  cell_matrix = [ 11, 11]
  cell_size = [ 0.200, 0.200]
  walls = wall.wallPublisher("wall_marker", cell_matrix, cell_size)
  map_data         = np.zeros( cell_matrix, dtype=int)
  map_data_colored = np.zeros( cell_matrix, dtype=int)

  try:
    loop = rospy.Rate(10) # 10[loop/s]の設定をする。
    while not rospy.is_shutdown():
#-----ここにプログラムを書く-----
  #-----地図情報を更新する-----
    #-----壁更新-----
      for iy in range(5):
        for ix in range(5):
          map_data[ iy*2+0, ix*2+0] = 1 # [ 偶数, 偶数]
          map_data[ iy*2+1, ix*2+1] = 2 # [ 奇数, 奇数]
          map_data[ iy*2+0, ix*2+1] = 3 # [ 偶数, 奇数]
          map_data[ iy*2+1, ix*2+0] = 4 # [ 奇数, 偶数]
  #-----マップ色変え＆マップ送信-----
      map_data_colored[ map_data == 0] = walls.WALL_INVISIBLE
      map_data_colored[ map_data == 1] = walls.WALL_BLUE
      map_data_colored[ map_data == 2] = walls.WALL_WHITE
      map_data_colored[ map_data == 3] = walls.WALL_RED
      map_data_colored[ map_data == 4] = walls.WALL_GREEN
      walls.setData( map_data_colored)
  #-----地図情報を表示する-----
      walls.publish()
#-----ここまで-----
      loop.sleep() # 10[loop/s]になるよう調整する。
  except KeyboardInterrupt: # try:中にCTRL-Cが押されればココを実行する。
    print("キーボード割り込み！CTRL-C　終了")
