#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
argv = sys.argv
argc = len(argv)

from PIL import Image
import random
import numpy as np
import rospy



def EmptyMaze( sx, sy): #迷路生成
  maze = [[ 0 for i in range(sx)] for ii in range(sy)]
  setOutsideWall( maze)
  return maze

def setOutsideWall( maze):
  sx = len( maze[ 0])
  sy = len( maze)
  for ix in range( sy):
    maze[    0][ ix] = 1
    maze[ sy-1][ ix] = 1
  for iy in range( sx):
    maze[ iy][    0] = 1
    maze[ iy][ sx-1] = 1

def poleDown( maze): #棒倒し法
  sx = len( maze[ 0])
  sy = len( maze)
  flag = False
  dire      = [ [ 0, 1], [ 1, 0], [ 0,-1], [-1, 0]] #壁を倒す候補[右上左下]
  dire_lim  = [ [ 0, 1], [ 1, 0], [ 0,-1]         ] #壁を倒す候補[右上左　]
  for iy in range( 2, sy-2, 2):
    for ix in range( 2, sx-2, 2): #　外周ではない偶数のみ選択
      maze[ iy][ ix] = 1 #偶数地点には壁
      while True:
        random.shuffle( dire) #壁を倒す候補をシャッフルする
        vy, vx = dire[ 0]     #一番最初の要素に決める。
        if maze[ iy+vy][ ix+vx] == 0: #候補先に壁がなければOK
          break
      maze[ iy+vy][ ix+vx] = 1 #候補先に壁

    if flag == False:
      dire = dire_lim
      flag = True

def printMaze( maze):
  sx = len( maze[ 0])
  sy = len( maze)
  for iy in range( sy):
    for ix in range( sx):
      if maze[ iy][ ix] == 0:
        print " ",
      elif maze[ iy][ ix] == 1:
        print "@",
    print "\n",

def outputMaze( maze, filename="test.png"):
  DPD = 20
  width  = len( maze[0]) * DPD
  height = len( maze)    * DPD
  BLACK = (0, 0, 0)
  WHITE = (255,255,255)
  img2 = Image.new('RGB', (width, height))
  for iy in range(height):
    for ix in range(width):
      img2.putpixel((ix, iy), WHITE)
      
  for iy in range(len(maze)):
    for ix in range(len(maze[0])):
      if maze[iy][ix]==1:
        if   ix%2==0 and iy%2==0:
          img2.putpixel((ix*DPD, iy*DPD), BLACK)
        elif ix%2==1 and iy%2==1:
          pass
        elif ix%2==0 and iy%2==1:
          for i in range(DPD*2):
            img2.putpixel((ix*DPD, iy*DPD-DPD+i), BLACK)
        elif ix%2==1 and iy%2==0:
          for i in range(DPD*2):
            img2.putpixel((ix*DPD-DPD+i, iy*DPD), BLACK)
          pass
  img2.save(filename)


if __name__ == '__main__':
  rospy.init_node("maze_creater")
  if argc == 1:
    sx = sy = 17 #default
  elif argc == 3:
    sx = int(argv[1])
    sy = int(argv[2])
  else:
    print("\n")
    print("argment Erorr! argument must be (0 or 2) ")
    print("Execute with default 2 argument (size_x = size_y = 17)")
    print("\n")

  if (sx % 2 == 0) or (sy % 2 == 0):
    sx += not (sx%2)
    sy += not (sy%2)
    print("\n")
    print("size_x and size_y must be OddNumber")
    print("I changed size by add +1  (sx, sy) = "),
    print sx, sy
    print("\n")

  maze = EmptyMaze( sx, sy)
  poleDown( maze)
  printMaze( maze)
  outputMaze( maze)
  
  rospy.set_param("/micro_mouse/maze/size/x", sx)
  rospy.set_param("/micro_mouse/maze/size/y", sy)
  rospy.set_param("/micro_mouse/maze/cell/x", 0.200)
  rospy.set_param("/micro_mouse/maze/cell/y", 0.200)
  rospy.set_param("/micro_mouse/maze/wall/x", 0.180)
  rospy.set_param("/micro_mouse/maze/wall/y", 0.020)
  rospy.set_param("/micro_mouse/maze/wall/z", 0.050)
  rospy.set_param("/micro_mouse/maze/pole/x", 0.020)
  rospy.set_param("/micro_mouse/maze/pole/y", 0.020)
  rospy.set_param("/micro_mouse/maze/pole/z", 0.050)
  rospy.set_param("/micro_mouse/maze/data", maze)
