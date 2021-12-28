cmake_minimum_required(VERSION 3.21)
project(footballdraft C)

set(CMAKE_C_STANDARD 23)

add_executable(footballdraft main.c player.c)

target_link_libraries(footballdraft m)