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
  vl = vr = dire = 0
  px = py = 1
  PI = math.pi
  action = -1

  try:
    loop = rospy.Rate(10) # 10[loop/s]の設定をする。
    while not rospy.is_shutdown():
#-----ここにプログラムを書く-----
  #-----センサー読み込み-----
      sensor = mouse.getSensor() < 0.2
  #-----ロボットの自己位置を更新する-----
      dire += vr; dire %= 4
      px += vl * math.cos( dire * PI/2)*2 # player(mouse)座標 x
      py += vl * math.sin( dire * PI/2)*2 # player(mouse)座標 y
      px = int(round(px)) # 整数化
      py = int(round(py)) # 整数化
  #-----行動選択(左手法)-----
      if   sensor[mouse.L] == False:
        action = 1
      elif sensor[mouse.L] == True and sensor[mouse.F] == False:
        action = 2
      elif sensor[mouse.L] == True and sensor[mouse.F] == True:
        action = 3
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
#-----ここまで-----
      loop.sleep() # 10[loop/s]になるよう調整する。
  except KeyboardInterrupt: # try:中にCTRL-Cが押されればココを実行する。
    print("キーボード割り込み！CTRL-C　終了")
