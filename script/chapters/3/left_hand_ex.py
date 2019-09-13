#!/usr/bin/env python
#coding: utf-8         # 日本語を使えるようにする

#-----include ros libraries-----
import roslib.packages
import sys
pk_path = roslib.packages.get_pkg_dir('micro_mouse')
sys.path.append(pk_path + '/script/lib')
import rospy  # include<ros/ros.h>のようなもの
import wall
import mouse
#-----include std libraries-----
import math
#-----include extends libraries
import numpy as np

if __name__ == '__main__': # int main()みたいな
  rospy.init_node("node_name") # ノード設定
#-----変数等の定義-----
  cell_matrix = [ 17, 17]
  cell_size = [ 0.200, 0.200]

  vl = vr = 0
  mx = my = theta = 0

  mouse = mouse.Mouse()
  walls = wall.wallPublisher("wall_marker", cell_matrix, cell_size)

  map_data = walls.getEmptyMazeMap( cell_matrix)
  map_data_colored = np.zeros( cell_matrix, dtype=int)

  vl = vr = 0
  mx = my = dire = 0
  try:
    loop = rospy.Rate(10) # 10[loop/s]の設定をする。
    while not rospy.is_shutdown():
#-----ここにプログラムを書く-----
  #-----ロボットの自己位置を更新する-----
      dire += vr; dire %= 4
      mx = int( round( mx + vl * math.cos( dire * math.pi/2)))
      my = int( round( my + vl * math.sin( dire * math.pi/2)))
      tx = mx*2 + 1  # trans_x (mouse position to maze position)
      ty = my*2 + 1  # trans_y (mouse position to maze position)
  #-----センサー読み込み-----
      sensor = mouse.getSensor() < 0.2
  #-----地図情報を更新する-----
    #-----壁更新-----
      for (i, s_rad) in enumerate(mouse.sensor_rad):
        wx = int( round( tx +  math.cos( dire*math.pi/2 + s_rad)))    # wall_x
        wy = int( round( ty +  math.sin( dire*math.pi/2 + s_rad)))    # wall_y
        rx = int( round( tx +  math.cos( dire*math.pi/2 + s_rad) *2))  # road_x
        ry = int( round( ty +  math.sin( dire*math.pi/2 + s_rad) *2))  # road_y
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
      map_data[ ty, tx] = 3 # 踏んだタイル
  #-----マップ色変え-----
      map_data_colored[ map_data == 0] = walls.WALL_INVISIBLE  # 何もない　  　は　透明
      map_data_colored[ map_data == 1] = walls.WALL_WHITE      # 壁　　　　　　は　白色
      map_data_colored[ map_data == 2] = walls.WALL_RED        # 仮想的な壁　　は　赤色
      map_data_colored[ map_data == 3] = walls.WALL_GREY       # 踏んだタイル　は　灰色
      walls.setData( map_data_colored)
  #-----行動選択(左手法)-----
      vl = vr = 0
      if sensor[4] == False:
        vl = 1; vr =  1
      elif sensor[4] == True and sensor[2] == True:
        vl = 0; vr = -1
      elif sensor[4] == True and sensor[2] == False:
        vl = 1; vr = 0
  #-----地図やロボット情報を表示する-----
      walls.publish()
  #-----ロボットを動かす-----
      if vr != 0:
        mouse.move( 0.0, vr * math.pi/2)
      if vl != 0:
        mouse.move( vl*0.2, 0.0, 10)
#-----ここまで-----
      loop.sleep() # 10[loop/s]になるよう調整する。
  except KeyboardInterrupt: # try:中にCTRL-Cが押されればココを実行する。
    print("キーボード割り込み！CTRL-C　終了")
