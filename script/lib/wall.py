#!/usr/bin/env python
#coding: utf-8         # 日本語を使えるようにする

import math
import rospy  # include<ros/ros.h>
from std_msgs.msg import ColorRGBA
from std_msgs.msg import UInt8MultiArray
from geometry_msgs.msg import Vector3
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray

class wallPublisher:
  def __init__( self, topic, matrix, size):
    self.colors = [ ColorRGBA( 0.0, 0.0, 0.0, 0.0),  # 0 Invisible
                    ColorRGBA( 1.0, 1.0, 1.0, 1.0),  # 1 White
                    ColorRGBA( 1.0, 0.0, 0.0, 1.0),  # 2 Red
                    ColorRGBA( 1.0, 0.5, 0.0, 1.0),  # 3 Orange
                    ColorRGBA( 1.0, 1.0, 0.0, 1.0),  # 4 Yellow
                    ColorRGBA( 0.0, 1.0, 0.0, 1.0),  # 5 Green
                    ColorRGBA( 0.0, 0.0, 1.0, 1.0),  # 6 Blue
                    ColorRGBA( 1.0, 0.0, 1.0, 1.0),  # 7 Purple
                    ColorRGBA( 0.5, 0.5, 0.5, 1.0)]  # 8 grey

    self.WALL_INVISIBLE = 0
    self.WALL_WHITE     = 1
    self.WALL_RED       = 2
    self.WALL_ORANGE    = 3
    self.WALL_YELLOW    = 4
    self.WALL_GREEN     = 5
    self.WALL_BLUE      = 6
    self.WALL_PURPLE    = 7
    self.WALL_GREY      = 8

    self.generate( matrix, size)
    self.pub_wall = rospy.Publisher( topic, MarkerArray, queue_size=10)

  def generate( self, matrix, size):
    (self.mx, self.my) = matrix
    (sx, sy) = size
    self.pole_sx = sx*0.1; self.wallx_sx = sx*0.85; self.wally_sx = sx*0.10; self.cell_sx = sx*0.85
    self.pole_sy = sy*0.1; self.wallx_sy = sy*0.10; self.wally_sy = sy*0.85; self.cell_sy = sy*0.85
    self.pole_sz =  0.200; self.wallx_sz =   0.200; self.wally_sz =   0.200; self.cell_sz =  0.050
    self.offset_x =-sx/2; self.offset_y =-sy/2; self.offset_z = -0.100;
    self.sx = sx
    self.sy = sy
    
    self.walls = MarkerArray()
    wall_ct = 0
    for iy in range( self.my):
      my = iy % 2
      wy = iy * self.sy / 2
      for ix in range( self.mx):
        mx = ix % 2
        num = self.mx*iy + ix
        wx = ix * self.sx / 2
        self.walls.markers.append( Marker())
        self.walls.markers[ -1].header.stamp = rospy.Time.now()
        self.walls.markers[ -1].header.frame_id = "odom"
        self.walls.markers[ -1].id = wall_ct
        self.walls.markers[ -1].ns = "wall_" + str( wall_ct)
        self.walls.markers[ -1].type = 1 # CUBE = 1
        self.walls.markers[ -1].action = 0 # ADD = MODIFY = 0
        self.walls.markers[ -1].pose.position.x = wx + self.offset_x
        self.walls.markers[ -1].pose.position.y = wy + self.offset_y
        self.walls.markers[ -1].pose.position.z =      self.offset_z
        self.walls.markers[ -1].pose.orientation.x = 0.0
        self.walls.markers[ -1].pose.orientation.y = 0.0
        self.walls.markers[ -1].pose.orientation.z = 0.0
        self.walls.markers[ -1].pose.orientation.w = 1.0
        if mx == 0 and my == 0:
          sx = self.pole_sx; sy = self.pole_sy; sz = self.pole_sz
        elif mx == 1 and my == 0:
          sx = self.wallx_sx; sy = self.wallx_sy; sz = self.wallx_sz
        elif mx == 0 and my == 1:
          sx = self.wally_sx; sy = self.wally_sy; sz = self.wally_sz
        else:
          sx = self.cell_sx; sy = self.cell_sy;sz = self.cell_sz

        self.walls.markers[ -1].scale = Vector3( sx, sy, sz)
        self.walls.markers[ -1].color = ColorRGBA( 1.0, 1.0, 1.0, 1.0)
        wall_ct += 1

  def setData( self, data):
    wall_ct = 0
    for iy in range( self.my):
      for ix in range( self.mx):
        color = self.colors[ data[ iy, ix]]
        self.walls.markers[ wall_ct].color = color
        wall_ct += 1

  def publish( self):
    self.pub_wall.publish( self.walls)
