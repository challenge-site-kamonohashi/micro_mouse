from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np



def spline(conf, x):
  a,b,c,d = conf
  y = a + b*(x) + c*(x**2) + d*(x**3)
  return y





x = np.array([0,1,2,3,9,8,6,7,8,9])
y = np.array([5,2,3,4,9,3,4,0,2,1])


deg = 5
point = 100
tck,u = interpolate.splprep([x,y],k=deg,s=0) 
u = np.linspace(0,1,num=point,endpoint=True) 
spline = interpolate.splev(u,tck)


#-----drawing-----
plt.figure(1)
plt.plot( x, y, "go")
plt.plot( spline[0], spline[1], "r-")

plt.pause(0.02)
plt.show()
