#!/usr/bin/env python
#coding: utf-8         # 日本語を使えるようにする

#-----include ros libraries-----
import roslib.packages
import sys
pk_path = roslib.packages.get_pkg_dir('micro_mouse')
sys.path.append(pk_path + '/script/lib')
import rospy  # include<ros/ros.h>のようなもの
import path
import wall
import mouse
import heatmap
import pathplanning

#-----include std libraries-----
import math
import time

#-----include extends libraries
import numpy as np


if __name__ == '__main__': # int main()みたいな
  rospy.init_node("node_name") # ノード設定

  use_sensor_num = [ 4, 2, 0]
  sensor = [ 0 for i in range( 4)]
  sensor_dire = [ 1, 0,-1,-2] # Left, Forward, Right, Back

  cell_matrix = [ 17, 17]
  cell_size = [ 0.200, 0.200]
  walls = wall.wallPublisher("wall_marker", cell_matrix, cell_size)
  heatmap_pub = heatmap.heatmapPublisher("heatmap", cell_matrix, cell_size)
  path_pub = path.pathPublisher("path_green", cell_size)
  mouse = mouse.Mouse( "cmd_vel",  ["scan/R",
                                    "scan/FR",
                                    "scan/F",
                                    "scan/FL",
                                    "scan/L"])
  maze_data = np.zeros( cell_matrix, dtype=int)
  map_data = np.zeros( cell_matrix, dtype=int)
  map_data_colored = np.zeros( cell_matrix, dtype=int)
  cost_map = np.zeros( cell_matrix, dtype=int)
  path_data = []

  for i in range(len(maze_data[0])):
    maze_data[ 0, i] = 1
    maze_data[-1, i] = 1
  for i in range(len(maze_data)):
    maze_data[i, 0] = 1
    maze_data[i,-1] = 1
  for i in range(len(maze_data[0])):
    for ii in range(len(maze_data)):
      if i%2==0 and ii%2==0:
        maze_data[i, ii] = 1

  vl = vr = 0
  mx = my = dire = 0
  try:
    loop = rospy.Rate(10) # 10[loop/s]の設定をする。
    while not rospy.is_shutdown():
#-----ここにプログラムを書く-----
  #-----センサー読み込み-----
      for (i, num) in enumerate(use_sensor_num):
        sensor[ i] = mouse.sensor[ num].data < 0.2
      sensor[ 3] = False
  #-----ロボットの自己位置を更新する-----
      dire += vr; dire %= 4
      mx = int( round( mx + vl * math.cos( dire * math.pi/2)))
      my = int( round( my + vl * math.sin( dire * math.pi/2)))
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
    #-----道更新-----
      map_data[ ty, tx] = 3 # 行き止まりでも交差点でもない場所
  #-----マップ色変え-----
      map_data_colored[ map_data == 0] = walls.WALL_INVISIBLE  # 何もない
      map_data_colored[ map_data == 1] = walls.WALL_WHITE      # 壁
      map_data_colored[ map_data == 2] = walls.WALL_RED        # 仮想的な壁
      map_data_colored[ map_data == 3] = walls.WALL_GREY       # 行き止まりでも交差点でもない(踏んだタイル)
      maze_data[ map_data==1] = 1
  #-----PathPlanning-----
      DIRECTIONS=[[1,0],[0,1],[-1,0],[0,-1]]
      cost_map = pathplanning.costmapByDijkstra( maze_data, start=[tx,ty], DIRECTIONS=DIRECTIONS)
      path_data = pathplanning.pathByCostmap( cost_map, start=[tx,ty], goal=[11, 9], DIRECTIONS=DIRECTIONS)
  #-----行動選択(左手法)-----
      vr = 0; vl = 0
      path_dire = path_data[0,:] - [ tx, ty]
      rad = int(round(math.atan2( path_dire[1], path_dire[0])/(math.pi/2)))
      rad = (rad - dire) % 4
      print(rad)
      if rad==0:
        vl = 1; vr = 0
      elif  0 < rad  and rad <= 2:
        vl = 0; vr = 1
      else:
        vl = 0; vr = -1
  #-----地図やロボット情報を表示する-----
      walls.setData( map_data_colored)
      path_pub.setData( path_data)
      walls.publish()
      path_pub.publish()
  #-----ロボットを動かす-----
      mouse.move( vl*0.2, vr*math.pi)
#-----ここまで-----
#      loop.sleep() # 10[loop/s]になるよう調整する。
  except KeyboardInterrupt: # try:中にCTRL-Cが押されればココを実行する。
    print("キーボード割り込み！CTRL-C　終了")
