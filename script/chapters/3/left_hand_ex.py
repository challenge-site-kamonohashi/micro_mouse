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
  PI = math.pi
  vl = vr = dire = 0
  px = py = 1
  action = -1

  map_data = walls.getEmptyMazeMap( cell_matrix)
  map_data_colored = np.zeros( cell_matrix, dtype=int)


  try:
    loop = rospy.Rate(10) # 10[loop/s]の設定をする。
    while not rospy.is_shutdown():
#-----ここにプログラムを書く-----
  #-----センサー読み込み-----
      sensor = mouse.getSensor() < 0.2
  #-----ロボットの自己位置を更新する-----
      dire += vr; dire %= 4
      px += vl * math.cos( dire * math.pi/2)*2 # player(mouse)座標 x
      py += vl * math.sin( dire * math.pi/2)*2 # player(mouse)座標 y
      px = int(round(px)) # 整数化
      py = int(round(py)) # 整数化
  #-----地図情報を更新する-----
    #-----壁更新-----
      for (i, s_rad) in enumerate(mouse.sensor_rad):
        wx = int( round( px +  math.cos( dire*PI/2 + s_rad)))     # wall_x
        wy = int( round( py +  math.sin( dire*PI/2 + s_rad)))     # wall_y
        rx = int( round( px +  math.cos( dire*PI/2 + s_rad) *2))  # road_x
        ry = int( round( py +  math.sin( dire*PI/2 + s_rad) *2))  # road_y
        if sensor[i] == True:
          map_data[ wy, wx] = 1 # 壁( white)
        if map_data[ py, px] == 0 and map_data[ wy, wx] == 0:
          if ( 0<=ry and ry<cell_matrix[0] and 0<=rx and rx<cell_matrix[1] and i!=3):
            if map_data[ ry, rx] != 0:
              map_data[ wy, wx] = 2 # 仮想的な壁
        sensor[i] = (map_data[ wy, wx] != 0)
  #-----道更新-----
      map_data[ py, px] = 3 # 踏んだタイル
  #-----マップ色変え-----
      map_data_colored[ map_data == 0] = walls.WALL_INVISIBLE  # 何もない　  　は　透明
      map_data_colored[ map_data == 1] = walls.WALL_WHITE      # 壁　　　　　　は　白色
      map_data_colored[ map_data == 2] = walls.WALL_RED        # 仮想的な壁　　は　赤色
      map_data_colored[ map_data == 3] = walls.WALL_GREY       # 踏んだタイル　は　灰色
      walls.setData( map_data_colored)
  #-----行動選択(左手法)-----
      if   sensor[mouse.L] == False:
        action = 1
      elif sensor[mouse.L] == True and sensor[mouse.F] == False:
        action = 2
      elif sensor[mouse.L] == True and sensor[mouse.F] == True:
        action = 3
  #-----地図やロボット情報を表示する-----
      walls.publish()
  #-----ロボットを動かす-----
      vl = vr = 0
      if action == 1:
        vl = 1; vr = 1
        mouse.move( 0.0, vr*PI/2)  # 駆動系(mouse.move())が複数あるのはあんまり良くない！
        mouse.move( vl*0.2,  0.0)  # 色々な場所に駆動系の記述があるとバグに繋がります.
      elif action == 2:
        vl = 1; vr = 0
        mouse.move( vl*0.2,  0.0)  # 今回はわかりやすさのために複数書いています.
      elif action == 3:
        vl = 0; vr =-1
        mouse.move( 0.0, vr*PI/2)
  #-----ロボットの自己位置を更新する-----
#-----ここまで-----
      loop.sleep() # 10[loop/s]になるよう調整する。
  except KeyboardInterrupt: # try:中にCTRL-Cが押されればココを実行する。
    print("キーボード割り込み！CTRL-C　終了")
