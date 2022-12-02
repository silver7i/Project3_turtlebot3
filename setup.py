from setuptools import setup

package_name = 'project3'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kim',
    maintainer_email='kim@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'track_marker5   = Project3_turtlebot3.script.track_marker5:main',
            'bluetooth_waypoint      = Project3_turtlebot3.script.bluetooth_waypoint:main',
            'img_compressed2raw      = Project3_turtlebot3.script.img_compressed2raw:main',
            'pub_tb3_pose2d      = Project3_turtlebot3.script.pub_tb3_pose2d:main',
            'pub_goal_msg      = Project3_turtlebot3.script.pub_goal_msg:main',
        ],
    },
)
