cmake_minimum_required(VERSION 3.8)
project(bt)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

ament_python_install_package(bt_nodes)

install(DIRECTORY bt_xml/
  DESTINATION share/${PROJECT_NAME}/bt_xml
)

install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)
install(PROGRAMS
  bt_nodes/bt_runner.py
  bt_nodes/battery_monitor.py
  bt_nodes/fire_safety.py
  bt_nodes/tf_publisher.py
  bt_nodes/navigate_to_server.py
  bt_nodes/obstacle_monitor.py
  bt_nodes/cmd_vel_converter.py
  bt_nodes/camera_colour_detector.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()