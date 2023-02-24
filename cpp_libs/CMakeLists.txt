cmake_minimum_required(VERSION 3.0)

set(CMAKE_CXX_STANDARD 17)

project(pyimg VERSION 0.1.0)

# Include dir
include_directories(include)

# Src
AUX_SOURCE_DIRECTORY(src SRC_FILES)

# Headers
set(PROJECT_SOURCE_DIR "src")
set(PROJECT_INCLUDE_DIR "include")

# Source files
set(SOURCE_FILES
    ${PROJECT_INCLUDE_DIR}/img_libs.hpp
    ${PROJECT_SOURCE_DIR}/img_libs.cpp
)

# Set up such that XCode organizes the files correctly
source_group(TREE ${CMAKE_CURRENT_SOURCE_DIR} FILES ${SOURCE_FILES})

# Add library
# add_library(img_libs SHARED ${SOURCE_FILES})
add_library(img_libs SHARED
  src/img_libs.cpp
  include/img_libs.hpp
)

# Include directories
target_include_directories(img_libs PRIVATE include)

# Install
install(TARGETS img_libs DESTINATION lib)

# Install the headers
# install(FILES include DESTINATION include)

# # Create base directory
# install(DIRECTORY include/automobile_bits DESTINATION include)