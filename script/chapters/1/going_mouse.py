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
  action_list = [ 1,2,2,2,3,2,3,2,1,2,1,2,3,2] # 1:左回転, 2:直進:, 3:右回転
  vl = 0
  vr = 0
#-----変数定義終了-----

  try:
    loop = rospy.Rate(10) # 10[loop/s]の設定をする。
    while not rospy.is_shutdown():
#-----ここにプログラムを書く-----
  #-----ロボットを動かす-----
      # mouse.move( 直進速度[ m/s], 回転速度[ rad/s])
      # 直進速度は 1[m/s]、回転速度は π /2 [ rad/s]が限界です。
      for action in action_list:
        vl = 0
        vr = 0
        if action == 1:
          vr =  math.pi/2
        elif action == 2:
          vl =  1
        elif action == 3:
          vr = -math.pi/2
        mouse.move(  vl, vr)
      break

#-----ここまで-----
      loop.sleep() # 10[loop/s]になるよう調整する。
  except KeyboardInterrupt: # 実行中(try:中)にCTRL-Cが押されればプログラムが終了する
    print("キーボード割り込み！CTRL-C　終了")
