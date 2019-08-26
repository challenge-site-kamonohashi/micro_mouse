import numpy as np



maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
maze = np.array(maze)

array_size = np.array(      [len(maze), len(maze      [0])])
map_size   = np.array((array_size-1) / 2)

cost = np.zeros(array_size, dtype=int)


inf = 100
dire = np.array([[ 0, 1], [ 1,  1], [ 1,0]])
weight =       [1, inf, 1]

for j in range(map_size[0]):
  for i in range(map_size[1]):
    mx = i*2 + 1
    my = j*2 + 1
    costs = []
    for d in dire:
      search_y = my - d[0]
      search_x = mx - d[1]
      if 0<search_x  and  0<search_y:
        costs.append(cost[search_y, search_x])
    if i==0 and j==0:
      cost[ my, mx] = 0
    else:
      cost[ my, mx] = min(costs)


    for d in dire:
      search_y = my + d[0]
      search_x = mx + d[1]
      if search_x<array_size[1]  and  search_y<array_size[0]:
        if maze[search_y, search_x] == 1:
          c = inf
        else:
          c = 1
        cost[ search_y, search_x] = cost[ my, mx] + c

print( cost)

for j in range(map_size[0]):
  for i in range(map_size[1]):
    mx = i*2 + 1
    my = j*2 + 1
    print( "%4d"%cost[my, mx]),
  print("")
      

