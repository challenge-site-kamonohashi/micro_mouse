import matplotlib.pyplot as plt
import numpy as np


def dotInLine(p0, p1, t):
  b01 = (1-t)*p0 + t*p1
  return b01

def bezierCurve(p0, p1, p2, t):
  b01 = dotInLine( p0, p1, t)
  b12 = dotInLine( p1, p2, t)
  b0112 = dotInLine( b01, b12, t)
  return b0112


def pltLine( p1, p2, option):
  plt.plot( [p1[0], p2[0]], [p1[1], p2[1]], option)


"""
plt.figure(1)

p0 = np.array([ 0, 0])
p1 = np.array([10, 0])
p2 = np.array([10,10])
buff = np.array([])
for t in np.arange(26)/25.0:
  p = bezierCurve( p0, p1, p2, t)

  #-----drawing-----
  buff = np.append( buff, [p]).reshape(-1, 2)
  plt.clf()
  plt.plot( p0[0], p0[1], 'bo')
  plt.plot( p1[0], p1[1], 'bo')
  plt.plot( p2[0], p2[1], 'bo')
  pltLine(dotInLine(p0, p1, t), dotInLine(p1, p2, t), "k-")
  plt.plot(buff[:,0], buff[:,1], "ro-")
  plt.pause(0.02)

plt.show()

"""
