from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler, DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PythonExpression, PathJoinSubstitution
import os
import xacro

def generate_launch_description():
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    world = os.path.join(get_package_share_directory(
        'warehouse'), 'worlds', 'small_warehouse_1.world')
 
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']), 
            launch_arguments={'world': world}.items()
    )
    
    urdf_path = os.path.join(
        get_package_share_directory('turtlebot3_description'),
        'models',
        'turtlebot3_waffle',
        'model.sdf'
    )
    
    robot_path = os.path.join(
        get_package_share_directory('turtlebot3_description'))
    
    urdf_file = os.path.join(robot_path,
                              'urdf',
                              'turtlebot3_waffle.urdf')

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()
  
    spawn_x_val = '0.0'
    spawn_y_val = '0.0'
    spawn_z_val = '0.0'

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name = 'robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time,
                     'robot_description': robot_desc
                    }],
    )                                                                                                                                                                                                                                                                                                                                                                                                               

    spawn_entity = Node(package='gazebo_ros',
                        executable='spawn_entity.py',
                        arguments=['-entity', 'turtlebot3_waffle',
                                   '-file', urdf_path,
                                   '-x', spawn_x_val,
                                   '-y', spawn_y_val,
                                   '-z', spawn_z_val,
                                   ],
                        output='screen')

    load_joint_state_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    ) 

    rviz2 = ExecuteProcess(cmd=['rviz2'],
                       output="screen")

    return LaunchDescription([
        gazebo,
        rviz2,
        robot_state_publisher,
        spawn_entity,
        ])