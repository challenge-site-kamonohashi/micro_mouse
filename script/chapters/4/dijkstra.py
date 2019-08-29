import numpy as np

def calc_cost( y, x):
  INF = 100
  result = 1
  if maze[y, x]==0:
    result = 1
  elif maze[y,x]==1:
    result = INF
  return result
np.set_printoptions(linewidth=200)



#-----------------------------------------------------------------------
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

INF = 100
array_size = np.array( [len(maze), len(maze[0])])
map_size   = np.array((array_size-1) / 2)
cost_map   = np.ones((array_size), dtype=int) * 0
cost_map[0,0] = 0
#directions = np.array([ [ 0,-1], [-1, 0]])
directions = np.array([[ 0, 1], [ 1,0], [ 0,-1], [-1, 0]])

for y in range(array_size[0]):
  for x in range(1,array_size[1]):
    costs = []
    for d in directions:
      search_y = y + d[0]
      search_x = x + d[1]
      if (0 <= search_x and search_x < array_size[1]) and \
         (0 <= search_y and search_y < array_size[0]):
        if ( INF <= calc_cost(y, x)):
          cost = INF
        else:
          cost = ( calc_cost(search_y, search_x) + cost_map[ y, x])
      costs.append( cost)
    print(costs)
    cost_map[y, x] += min(costs)
      


print(cost_map)



