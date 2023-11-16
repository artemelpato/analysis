cmake_minimum_required(VERSION 3.15)
project(assignment)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS 1)
set(CMAKE_CXX_FLAGS "-Wall -Werror -Wextra -pedantic")

find_package(ROOT REQUIRED)
find_package(fmt REQUIRED)

include_directories(include)

add_library(SignalExtractor SHARED src/SignalExtractor.cpp)
target_link_libraries(SignalExtractor ROOT::RIO fmt::fmt)
