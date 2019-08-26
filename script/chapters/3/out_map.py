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
  sensor = [ 0 for i in range( 4)]
  sensor_dire = [ 1, 0,-1,-2] # Left, Forward, Right, Back

  cell_matrix = [ 17, 17]
  cell_size = [ 0.500, 0.500]
  walls = wall.wallPublisher("wall_marker", cell_matrix, cell_size)
  mouse = mouse.Mouse( "cmd_vel",  ["scan/R",
                                    "scan/FR",
                                    "scan/F",
                                    "scan/FL",
                                    "scan/L"])
  map_data = np.zeros( cell_matrix, dtype=int)
  map_data_colored = np.zeros( cell_matrix, dtype=int)

  vl = vr = 0
  mx = my = dire = 0
  try:
    loop = rospy.Rate(10) # 10[loop/s]の設定をする。
    while not rospy.is_shutdown():
#-----ここにプログラムを書く-----
  #-----センサー読み込み-----
      for (i, num) in enumerate(use_sensor_num):
        sensor[ i] = mouse.sensor[ num].data < 1.0
      sensor[ 3] = False
  #-----地図情報を更新する-----
    #-----壁更新-----
      tx = mx*2 + 1
      ty = my*2 + 1
      for (i,s_dire) in enumerate(sensor_dire):
        wx = int( round( tx +  math.cos( (dire + s_dire) * math.pi/2)))
        wy = int( round( ty +  math.sin( (dire + s_dire) * math.pi/2)))
        rx = int( round( tx +  math.cos( (dire + s_dire) * math.pi/2)*2))
        ry = int( round( ty +  math.sin( (dire + s_dire) * math.pi/2)*2))
        if sensor[i] == True:
          map_data[ wy, wx] = 1 # 壁( white)
        if map_data[ ty, tx] == 0 and map_data[ wy, wx] == 0:
          if not (rx < 0 or ry < 0 or cell_matrix[0] <= rx or cell_matrix[1] <= ry or i==3):
            if map_data[ ry, rx] != 0:
              map_data[ wy, wx] = 2 # 仮想的な壁
        sensor[i] = (map_data[ wy, wx] != 0)
      print sensor
      print mx, my, dire
      print "----------------"
    #-----道更新-----
      wall = sum( sensor)
      if wall== 3:
        color = 3 # 行き止まり
      elif wall <= 1:
        color = 4 # 交差点
      else:
        color = 5 # 行き止まりでも交差点でもない場所
      map_data[ ty, tx] = color
  #-----マップ色変え＆マップ送信-----
      map_data_colored[ map_data == 0] = walls.WALL_INVISIBLE  # 何もない
      map_data_colored[ map_data == 1] = walls.WALL_WHITE      # 壁
      map_data_colored[ map_data == 2] = walls.WALL_RED        # 仮想的な壁
      map_data_colored[ map_data == 3] = walls.WALL_GREEN      # 行き止まり
      map_data_colored[ map_data == 4] = walls.WALL_ORANGE     # 交差点
      map_data_colored[ map_data == 5] = walls.WALL_GREY       # 行き止まりでも交差点でもない(踏んだタイル)
      walls.setData( map_data_colored)
  #-----行動選択(左手法)-----
      vl = vr = 0
      if sensor[0] == False:
        vl = 1; vr =  1
      elif sensor[0] == True and sensor[1] == True:
        vl = 0; vr = -1
      elif sensor[0] == True and sensor[1] == False:
        vl = 1; vr = 0
  #-----地図やロボット情報を表示する-----
      walls.publish()
  #-----ロボットを動かす-----
      if vr != 0:
        mouse.move( 0.0, vr * math.pi/2)
      if vl != 0:
        mouse.move( vl, 0.0, 10)
  #-----ロボットの自己位置を更新する-----
      dire += vr; dire %= 4
      mx = int( round( mx + vl * math.cos( dire * math.pi/2)))
      my = int( round( my + vl * math.sin( dire * math.pi/2)))
#-----ここまで-----
      loop.sleep() # 10[loop/s]になるよう調整する。
  except KeyboardInterrupt: # try:中にCTRL-Cが押されればココを実行する。
    print("キーボード割り込み！CTRL-C　終了")
