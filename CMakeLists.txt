cmake_minimum_required(VERSION 3.21)
project(footballsim C)

set(CMAKE_C_STANDARD 99)

add_executable(footballgame main.c player.c team.c game.c csv_parser.c draft.c)

target_link_libraries(footballgame m)