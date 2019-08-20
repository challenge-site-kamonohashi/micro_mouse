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

  mouse = mouse.Mouse( "cmd_vel",  ["scan/R",  # 0 センサの管理番号
                                    "scan/FR", # 1
                                    "scan/F",  # 2
                                    "scan/FL", # 3
                                    "scan/L"]) # 4
#-----変数定義-----
  # mouseには5つのセンサが搭載されています。
  # それぞれのセンサ値を管理するための配列変数sensorを定義する。
  sensor = [0 for i in range( 5)]
#-----変数定義終了-----

  try:
    loop = rospy.Rate(10) # 10[loop/s]の設定をする。
    while not rospy.is_shutdown():
#-----ここにプログラムを書く-----
     #-----センサー読み込み-----
      # mouse.sensor[管理番号]で、壁までの「距離」が取得できる。
      # また、(距離 < 1.0)で、[距離]を[ブール値]に変える
      for i in range(5):
        sensor[ i] = (mouse.sensor[ i].data < 1.0)
  #-----ロボットを動かす-----
      # mouse.move( 直進速度[ m/s], 回転速度[ rad/s])
      # 直進速度は 1[m/s]、回転速度は π /2 [ rad/s]が限界です。
      if sensor[ 2] == 0:
        print("壁がない、前に進もう")
        mouse.move(  1,  0.0)
      else:
        print("壁がある、左回転しよう")
        mouse.move(  0,  math.pi/2)
#-----ここまで-----
      loop.sleep() # 10[loop/s]になるよう調整する。
  except KeyboardInterrupt: # 実行中(try:中)にCTRL-Cが押されればプログラムが終了する
    print("キーボード割り込み！CTRL-C　終了")
