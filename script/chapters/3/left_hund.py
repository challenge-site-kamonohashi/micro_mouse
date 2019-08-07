#!/usr/bin/env python
#coding: utf-8         # 日本語を使えるようにする

import roslib.packages
pk_path = roslib.packages.get_pkg_dir('micro_mouse')
import sys
sys.path.append(pk_path + '/script/lib')

import math
import numpy as np
import rospy  # include<ros/ros.h>のようなもの
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

import wall
import mouse


if __name__ == '__main__': # int main()みたいな
  rospy.init_node("node_name") # ノード設定

  use_sensor_num = [ 4, 2, 0]
  sensor = [ 0 for i in range( 3)]
  sensor_dire = [ 1, 0,-1]

  cell_matrix = [ 17, 17]
  cell_size = [ 0.500, 0.500]
  walls = wall.wallPublisher("wall_marker", cell_matrix, cell_size)
  mouse = mouse.Mouse( "cmd_vel",  ["scan/R",
                                    "scan/FR",
                                    "scan/F",
                                    "scan/FL",
                                    "scan/L"])
  map_data = np.zeros( cell_matrix, dtype="int")

  vl = vr = 0
  mx = my = theta = 0
  try:
    loop = rospy.Rate(10) # 10[loop/s]の設定をする。
    while not rospy.is_shutdown():
#-----ここにプログラムを書く-----

  #-----センサー読み込み-----
      for (i, num) in enumerate(use_sensor_num):
        sensor[ i] = mouse.sensor[ num].data < 1.0
  #-----検知した壁を地図に反映させる
      for (i,dire) in enumerate(sensor_dire):
        if sensor[i] == True:
          wx = int( round( mx*2+1  +  math.cos( (theta + dire) * math.pi/2)))
          wy = int( round( my*2+1  +  math.sin( (theta + dire) * math.pi/2)))
          map_data[ wy, wx] = 1
  #-----地図情報等を表示する-----
      print mx, my, theta
      walls.setData( map_data)
      walls.publish()
  #-----行動選択(左手法)-----
      vl = vr = 0
      if sensor[0] == False:
        vl = 1; vr =  1
      elif sensor[0] == True and sensor[1] == True:
        vl = 0; vr = -1
      elif sensor[0] == True and sensor[1] == False:
        vl = 1; vr = 0
  #-----ロボットを動かす-----
      if vr != 0:
        mouse.move(0.0, vr * math.pi/2, 10)
      if vl != 0:
        mouse.move( vl, 0.0, 10)
  #-----ロボットの自己位置を更新する-----
      theta += vr; theta %= 4
      mx = int( round( mx + vl * math.cos( theta * math.pi/2)))
      my = int( round( my + vl * math.sin( theta * math.pi/2)))

#-----ここまで-----
      loop.sleep() # 10[loop/s]になるよう調整する。
  except KeyboardInterrupt: # try:中にCTRL-Cが押されればココを実行する。
    print("キーボード割り込み！CTRL-C　終了")
