define kinect ranger
(
  # generic model properties
  pose [ 0.0 0.0 0.0 0.0 ]
  size [ 0.10 0.10 0.10]
  origin [ 0.0 0.0 0.0 0.0 ]
  color "white"

  sensor
  (
    range [ 0.15  0.3]
    fov 180.0
    samples 180
    color "red"
  )
)

define turtlebot position
(
  pose [ 0.0 0.0 0.0 0.0 ]

  odom_error [0.03 0.03 999999 999999 999999 0.02]

  size [ 0.100 0.100 0.200 ]
  origin [ 0.0 0.0 0.0 0.0 ]
  gui_nose 1
  drive "diff"
  color "red"
  
  kinect(pose [ 0.0 0.0 -0.1 0.0 ])
)
