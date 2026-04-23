cmake_minimum_required(VERSION 3.8)
project(gazebo_worlds)

find_package(ament_cmake REQUIRED)

# Install world files
install(DIRECTORY worlds/
  DESTINATION share/${PROJECT_NAME}/worlds
)

# Install model files (for future use)
install(DIRECTORY models/
  DESTINATION share/${PROJECT_NAME}/models
  OPTIONAL  # won't error if models/ is empty or missing
)

ament_package()
