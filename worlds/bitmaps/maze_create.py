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

def outPngMaze( maze, filename="test.png"):
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

def outBinMaze( maze, filename="test.txt"):
  with open(filename, mode='w') as f:
    f.write("[\n")
    for iy in range(len(maze)):
      f.write("[")
      for ix in range(len(maze[0])-1):
        f.write(str(maze[iy][ix])+",")
      else:
        f.write(str(maze[iy][-1])+"],\n")
    f.write("]")
          
        


def outWorldMaze( maze, filename="test"):
  sx = len(maze[0])
  sy = len(maze)
  with open("./../"+filename+".world", mode='w') as f:
    f.write('include "map.inc"\n')
    f.write('include "turtlebot.inc"\n')
    f.write('\n')
    f.write('# time to pause (in GUI mode) or quit (in headless mode (-g)) the simulation\n')
    f.write('quit_time 36000 # 10 hour of simulated time\n')
    f.write('paused 1\n')
    f.write('resolution 0.005\n')
    f.write('\n')
    f.write('window\n')
    f.write('(\n')
    f.write('  size [ '+str(sx*20.0)+' '+str(sy*20.0)+'] # in pixels\n')
    f.write('  scale 180.000   # pixels per meter\n')
    f.write('  center [ 0  0 ]\n')
    f.write('  rotate [ 0  0 ]\n')
    f.write('\n')
    f.write('  show_data 1              # 1=on 0=off\n')
    f.write(')\n')
    f.write('\n')
    f.write('# load an environment bitmap\n')
    f.write('floorplan\n')
    f.write('(\n')
    f.write('  name "test_stage"\n')
    f.write('  size [ '+str((sx-1)/10.0)+' '+str((sy-1)/10.0)+' 0.200]\n')
    f.write('  pose [0 0 0 0]\n')
    f.write('  bitmap "bitmaps/' +str(filename)+'.png"\n')
    f.write('  obstacle_return 1\n')
    f.write(')\n')
    f.write('\n') 
    f.write('turtlebot( pose [ '+str((sx-3)/-20.0)+' '+str((sy-3)/-20.0)+' 0.0 0.0 ] name "mouse")\n')



if __name__ == '__main__':
  rospy.init_node("maze_creater")
  if argc == 1:
    sx = sy = 17 #default
    filename="test"
  elif argc == 4:
    sx = int(argv[1])
    sy = int(argv[2])
    filename = str(argv[3])
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
  outPngMaze( maze, filename=filename+".png")
  outBinMaze( maze, filename=filename+".txt")
  outWorldMaze( maze, filename=filename)
  
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
