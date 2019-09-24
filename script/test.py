import numpy as np


class Player:
  def __init__(self, name, color):
    self.name = name
    self.color = color
    
  def play(self, board, available_list):
    if len(available_list)==0:
      return -1
    return 0


class Rule:
  def __init__( self, size):
    self.size = size

  def generateAvailable( self, board):
    matrix = board.matrix
    available_matrix = np.zeros( self.size)
    sx, sy = self.size
    dire = np.array([[-1, 1], [ 0, 1], [ 1, 1],
                     [-1, 0], [ 0, 0], [ 1, 0],
                     [-1,-1], [ 0,-1], [ 1,-1]])
    for y in range(sy):
      for x in range(sx):
        x, y = np.array(pos)
        for d in dire:
          begin_color = 0
	  for dist in range(8):
            xd, yd, = pd = pos + d*dist
	    now_color = matrix[yd, xd]
            if putAvailable( pd):
              break
	    if now_color == 0:
	      break
            if not begin_color == 0:
              if not now_color == begin_color:
                available_matrix[x, y] = 1
                break
            begin_color = now_color




    return [[0,0], [0,1], [0,2]]

  def putAvailable( self, pos)
    x, y = pos
    sx, sy = self.size
    return 0<=x and x<sx and 0<=y and y<sy
    

  def jadge( self, board, choose, color):
    pass


class Board:
  def __init__( self, size, colors):
    self.size = size
    self.colors = colors
    self.matrix = np.zeros(size, dtype=int)
    self.initBoard()

  def initBoard( self): 
    x = int(round(size[0]/2))
    y = int(round(size[1]/2))
    self.matrix[y  , x  ] = self.colors[0]
    self.matrix[y-1, x-1] = self.colors[0]
    self.matrix[y-1, x  ] = self.colors[1]
    self.matrix[y  , x-1] = self.colors[1]


def printBoard( matrix, size):
  matrix_view = np.zeros( size, dtype=str) 
  matrix_view[ matrix==1] = "O"
  matrix_view[ matrix==2] = "X"
  matrix_view[ matrix==0] = "-"
  print("----------------")
  sx, sy = size
  for iy in range(sy):
    for ix in range(sx):
      print(matrix_view[iy, ix]),
    print("")



size = sx, sy = [ 8, 8]
board = Board( size, [1, 2])
rule = Rule( size)
player = [Player("P1",1), Player("P2",2)]

for turn in range(sy*sx-4):
  for p in player:
    color = p.color
    available_list = rule.generateAvailable( board, color)
#    choose = p.play(board, available_list)
#    rule.jadge(board, choose, color)
    printBoard( board.matrix, size)
