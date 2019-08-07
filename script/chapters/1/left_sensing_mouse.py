#!/usr/bin/env python
#coding: utf-8         # 日本語を使えるようにする

import roslib.packages
pk_path = roslib.packages.get_pkg_dir('micro_mouse')
import sys
sys.path.append(pk_path + '/script/lib')

import math
import rospy  # include<ros/ros.h>のようなもの

import mouse


if __name__ == '__main__': # int main()みたいな
  rospy.init_node("node_name") # ノード設定

  mouse = mouse.Mouse( "cmd_vel",  ["scan/R",
                                    "scan/FR",
                                    "scan/F",
                                    "scan/FL",
                                    "scan/L"])
#-----変数定義-----
  # mouseには5つのセンサが搭載されています。
  # それぞれのセンサ値を管理するための配列変数sensorを定義する。
  sensor = [0 for i in range( 5)]
  vl = vr = 0
#-----変数定義終了-----

  try:
    loop = rospy.Rate(10) # 10[loop/s]の設定をする。
    while not rospy.is_shutdown():
#-----ここにプログラムを書く-----
  #-----センサー読み込み-----
      # mouse.sensor[ 管理番号 ] で、壁までの「距離」が取得できる。
      # また、 ( 距離 < 1.0) で、 [ 距離 ] を [ ブール値 ] に変える
      for i in range(5):
        sensor[ i] = mouse.sensor[ i].data < 1.0
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
        mouse.move( vl, 0.0, 10)
#-----ここまで-----
      loop.sleep() # 10[loop/s]になるよう調整する。
  except KeyboardInterrupt: # try:中にCTRL-Cが押されればココを実行する。
    print("キーボード割り込み！CTRL-C　終了")
