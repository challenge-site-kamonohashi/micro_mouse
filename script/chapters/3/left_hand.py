#!/usr/bin/env python
#coding: utf-8         # 日本語を使えるようにする

#-----include ros libraries-----
import roslib.packages
import sys
pk_path = roslib.packages.get_pkg_dir('micro_mouse')
sys.path.append(pk_path + '/script/lib')
import rospy
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

  try:
    loop = rospy.Rate(10) # 10[loop/s]の設定をする。
    while not rospy.is_shutdown():
#-----ここにプログラムを書く-----
  #-----センサー読み込み-----
      sensor = mouse.getSensor() < 0.2
  #-----行動選択(左手法)-----
      vl = vr = 0
      if sensor[4] == False:
        vl = 1; vr =  1
      elif sensor[4] == True and sensor[2] == True:
        vl = 0; vr = -1
      elif sensor[4] == True and sensor[2] == False:
        vl = 1; vr = 0
  #-----ロボットを動かす-----
      if vr != 0:
        mouse.move(0.0, vr * math.pi/2, 10)
      if vl != 0:
        mouse.move( vl*0.2, 0.0, 10)
  #-----ロボットの自己位置を更新する-----
      theta += vr; theta %= 4
      mx = int( round( mx + vl * math.cos( theta * math.pi/2)))
      my = int( round( my + vl * math.sin( theta * math.pi/2)))
#-----ここまで-----
      loop.sleep() # 10[loop/s]になるよう調整する。
  except KeyboardInterrupt: # try:中にCTRL-Cが押されればココを実行する。
    print("キーボード割り込み！CTRL-C　終了")
