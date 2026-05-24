# Copyright 2026 pgonzal@fi.uba.ar
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # -----------------------------
    # Configuración general
    # -----------------------------

    # Argumento del tiempo simulado
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)

    # -----------------------------
    # Recursos y entorno
    # -----------------------------
    # Primero que todo, setear donde gazebo va a buscar los plugins de simulación (por ejemplo, el plugin de sensores)
    os.environ['GZ_SIM_SYSTEM_PLUGIN_PATH'] = (
        '/opt/ros/jazzy/opt/gz_sim_vendor/lib/gz-sim-8/plugins:'
        + os.environ.get('GZ_SIM_SYSTEM_PLUGIN_PATH', '')
    )

    # Defino la ubicación de los modelos (por ejemplo un escritorio que quiera poner en el .world de gazebo)
    gazebo_models_path = 'models'
    pkg_share_gazebo = FindPackageShare('clase5').find('clase5')    
    gazebo_models_path = os.path.join(pkg_share_gazebo, gazebo_models_path)
    
    # Si la variable ya existe, la extendemos; si no, la creamos
    set_env_vars_resources = SetEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        gazebo_models_path
    )

    # -----------------------------
    # Construcción robot_description
    # -----------------------------
    # Obtener URDF via xacro
    robot_description_content = Command(
        [
            FindExecutable(name='xacro'),
            ' ',
            PathJoinSubstitution(
                [FindPackageShare('clase5'),
                 'urdf', LaunchConfiguration('xacro_file')]
            ),
        ]
    )    
    robot_description = {'robot_description': robot_description_content}

    # -----------------------------
    # Nodos de infraestructura
    # -----------------------------
    # Nodo para publicar el estado del robot: 
    # se encarga de publicar la descripción del robot y su estado en ROS2,
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # Nodo para spawnear el robot en Gazebo: 
    # se encarga de crear la entidad del robot en el mundo simulado, 
    # usando la descripción URDF generada por xacro.
    gz_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=['-topic', 'robot_description',
                    '-name', 'robot_name',
                    '-allow_renaming', 'true', 
                    '-x', '0.0',      # Coordenada X
                    '-y', '0.0',      # Coordenada Y
                    '-z', '0.55'      # Coordenada Z (0.55 es la altura del escritorio)
                    ],

    )

    # Nodo para el broadcaster de estado de los joints: 
    # se encarga de publicar la posición actual de los joints del robot.
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
    )

    # El controlador de esfuerzos se define en el archivo ros2_controllers.yaml, 
    # donde se especifica que el tipo es "effort_controllers/JointGroupEffortController" 
    # y se le asignan los joints a controlar (en este caso, joint1 y joint2).
    robot_controllers = PathJoinSubstitution(
        [
            FindPackageShare('clase5'),
            'config',
            'ros2_controllers.yaml',
        ]
    )    

    # Nodo para el controlador de esfuerzos: se encarga de aplicar los torques en los ejes del robot.
    effort_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'torque_input',
            '--param-file',
            robot_controllers
            ],
    )    

    # Nodo para el bridge entre ROS2 y Gazebo
    # Se comparte el clock entre Gazebo y ROS2 para que los nodos de ROS2 puedan usarlo como referencia temporal
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                   '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU'],
        output='screen'
    )
    
    # -----------------------------
    # Nodos de usuario
    # -----------------------------
    # Nodo para visualizar el robot en RViz
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=['-d', os.path.join(get_package_share_directory('clase5'), 'config', 'display.rviz')]
    )
    
    # Nodo para la GUI de aplicación de torque
    gui_effort_reference_node = Node(
        package='clase5',
        executable='gui_apply_torque.py',
        name='gui_apply_torque',
        output='screen',
    )

    return LaunchDescription([
        # Launch arguments: permiten parametrizar el launcher desde línea de comandos.
        DeclareLaunchArgument(
            'use_sim_time',
            default_value=use_sim_time,
            description='True para usar un clock simulado'),
        DeclareLaunchArgument(
            'xacro_file',
            default_value='dp.xacro',
            description='Archivo de definición del robot'
        ),
        DeclareLaunchArgument(
            'world_name',
            default_value='mundo_vacio.world',
            description='Nombre del archivo del mundo para Gazebo'
        ),

        # Environment setup: configuración del entorno antes de lanzar procesos.
        set_env_vars_resources, # Setea las variables de entorno para los modelos de gazebo

        # Include external launch: permite reutilizar launchers existentes, como el de Gazebo.
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [PathJoinSubstitution([
                    FindPackageShare('ros_gz_sim'),
                    'launch',
                    'gz_sim.launch.py'
                ])]
            ),
            launch_arguments=[(
                'gz_args',
                [
                    '-r -v 1 ',
                    PathJoinSubstitution([
                        FindPackageShare('clase5'),
                        'worlds',
                        LaunchConfiguration('world_name')
                    ]),
                    ' --gui-config ',
                    PathJoinSubstitution([
                        FindPackageShare('clase5'),
                        'config',
                        'gazebo.config'
                    ])
                ]
            )]
        ),

        # Event handlers: permiten coordinar secuencias temporales.
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=gz_spawn_entity,
                on_exit=[joint_state_broadcaster_spawner],
            )
        ),

        # Infrastructure nodes: son nodos necesarios para que el sistema funcione internamente.
        effort_controller_spawner,
        bridge,
        node_robot_state_publisher,
        gz_spawn_entity,

        # User interaction nodes: interfaces para operar o visualizar el sistema.
        rviz_node,
        gui_effort_reference_node,
    ])    
