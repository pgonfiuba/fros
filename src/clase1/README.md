# Clase 1

Primera introducció a ROS 2 con rosbags

## Compilación

```bash
colcon build --packages-select clase1 --symlink-install
source install/setup.bash
```

## Analisis de nodos

Pueden ejecutar dos nodos con:
```
ros2 launch clase1 node_analysis.launch.py
```

## Qué explorar
- Ver los nodos que se ejecutan con `ros2 node list`, `ros2 node info [nodo]`.
- Ver que se publica con los tópicos `ros2 topic list`, `ros2 topic info [topico]`.
- Ver que pasa si publicamos en un nodo: `ros2 topic pub -r 1 /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0,y: 0.0,z: 0.4}}"`
- Ver en los paneles de RQT la misma información.


## Descarga y analisis de rosbag

Descar el launchfile que vamos a usar:

```
mkdir r2b_robotarm
curl -L 'https://api.ngc.nvidia.com/v2/resources/org/nvidia/team/isaac/r2bdataset2024/1/files?redirect=true&path=r2b_robotarm/r2b_robotarm_0.mcap' -o 'r2b_robotarm/r2b_robotarm_0.mcap'
curl -L 'https://api.ngc.nvidia.com/v2/resources/org/nvidia/team/isaac/r2bdataset2024/1/files?redirect=true&path=r2b_robotarm/metadata.yaml' -o 'r2b_robotarm/metadata.yaml'
```

## Qué explorar
- Para saber qué información tiene: ros2 bag info r2b_robotarm
- Para ver los datos: ros2 run rqt_bag rqt_bag r2b_robotarm/
- Para reproducir el rosbag: ros2 bag play r2b_robotarm -r0.5
