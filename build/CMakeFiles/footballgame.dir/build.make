# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/alex/footballsim

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/alex/footballsim/build

# Include any dependencies generated for this target.
include CMakeFiles/footballgame.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/footballgame.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/footballgame.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/footballgame.dir/flags.make

CMakeFiles/footballgame.dir/main.c.o: CMakeFiles/footballgame.dir/flags.make
CMakeFiles/footballgame.dir/main.c.o: ../main.c
CMakeFiles/footballgame.dir/main.c.o: CMakeFiles/footballgame.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/alex/footballsim/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/footballgame.dir/main.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/footballgame.dir/main.c.o -MF CMakeFiles/footballgame.dir/main.c.o.d -o CMakeFiles/footballgame.dir/main.c.o -c /home/alex/footballsim/main.c

CMakeFiles/footballgame.dir/main.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/footballgame.dir/main.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/alex/footballsim/main.c > CMakeFiles/footballgame.dir/main.c.i

CMakeFiles/footballgame.dir/main.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/footballgame.dir/main.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/alex/footballsim/main.c -o CMakeFiles/footballgame.dir/main.c.s

CMakeFiles/footballgame.dir/coach.c.o: CMakeFiles/footballgame.dir/flags.make
CMakeFiles/footballgame.dir/coach.c.o: ../coach.c
CMakeFiles/footballgame.dir/coach.c.o: CMakeFiles/footballgame.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/alex/footballsim/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object CMakeFiles/footballgame.dir/coach.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/footballgame.dir/coach.c.o -MF CMakeFiles/footballgame.dir/coach.c.o.d -o CMakeFiles/footballgame.dir/coach.c.o -c /home/alex/footballsim/coach.c

CMakeFiles/footballgame.dir/coach.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/footballgame.dir/coach.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/alex/footballsim/coach.c > CMakeFiles/footballgame.dir/coach.c.i

CMakeFiles/footballgame.dir/coach.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/footballgame.dir/coach.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/alex/footballsim/coach.c -o CMakeFiles/footballgame.dir/coach.c.s

CMakeFiles/footballgame.dir/player.c.o: CMakeFiles/footballgame.dir/flags.make
CMakeFiles/footballgame.dir/player.c.o: ../player.c
CMakeFiles/footballgame.dir/player.c.o: CMakeFiles/footballgame.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/alex/footballsim/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building C object CMakeFiles/footballgame.dir/player.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/footballgame.dir/player.c.o -MF CMakeFiles/footballgame.dir/player.c.o.d -o CMakeFiles/footballgame.dir/player.c.o -c /home/alex/footballsim/player.c

CMakeFiles/footballgame.dir/player.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/footballgame.dir/player.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/alex/footballsim/player.c > CMakeFiles/footballgame.dir/player.c.i

CMakeFiles/footballgame.dir/player.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/footballgame.dir/player.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/alex/footballsim/player.c -o CMakeFiles/footballgame.dir/player.c.s

CMakeFiles/footballgame.dir/team.c.o: CMakeFiles/footballgame.dir/flags.make
CMakeFiles/footballgame.dir/team.c.o: ../team.c
CMakeFiles/footballgame.dir/team.c.o: CMakeFiles/footballgame.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/alex/footballsim/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building C object CMakeFiles/footballgame.dir/team.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/footballgame.dir/team.c.o -MF CMakeFiles/footballgame.dir/team.c.o.d -o CMakeFiles/footballgame.dir/team.c.o -c /home/alex/footballsim/team.c

CMakeFiles/footballgame.dir/team.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/footballgame.dir/team.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/alex/footballsim/team.c > CMakeFiles/footballgame.dir/team.c.i

CMakeFiles/footballgame.dir/team.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/footballgame.dir/team.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/alex/footballsim/team.c -o CMakeFiles/footballgame.dir/team.c.s

CMakeFiles/footballgame.dir/game.c.o: CMakeFiles/footballgame.dir/flags.make
CMakeFiles/footballgame.dir/game.c.o: ../game.c
CMakeFiles/footballgame.dir/game.c.o: CMakeFiles/footballgame.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/alex/footballsim/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building C object CMakeFiles/footballgame.dir/game.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/footballgame.dir/game.c.o -MF CMakeFiles/footballgame.dir/game.c.o.d -o CMakeFiles/footballgame.dir/game.c.o -c /home/alex/footballsim/game.c

CMakeFiles/footballgame.dir/game.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/footballgame.dir/game.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/alex/footballsim/game.c > CMakeFiles/footballgame.dir/game.c.i

CMakeFiles/footballgame.dir/game.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/footballgame.dir/game.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/alex/footballsim/game.c -o CMakeFiles/footballgame.dir/game.c.s

CMakeFiles/footballgame.dir/csv_parser.c.o: CMakeFiles/footballgame.dir/flags.make
CMakeFiles/footballgame.dir/csv_parser.c.o: ../csv_parser.c
CMakeFiles/footballgame.dir/csv_parser.c.o: CMakeFiles/footballgame.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/alex/footballsim/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Building C object CMakeFiles/footballgame.dir/csv_parser.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/footballgame.dir/csv_parser.c.o -MF CMakeFiles/footballgame.dir/csv_parser.c.o.d -o CMakeFiles/footballgame.dir/csv_parser.c.o -c /home/alex/footballsim/csv_parser.c

CMakeFiles/footballgame.dir/csv_parser.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/footballgame.dir/csv_parser.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/alex/footballsim/csv_parser.c > CMakeFiles/footballgame.dir/csv_parser.c.i

CMakeFiles/footballgame.dir/csv_parser.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/footballgame.dir/csv_parser.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/alex/footballsim/csv_parser.c -o CMakeFiles/footballgame.dir/csv_parser.c.s

CMakeFiles/footballgame.dir/draft.c.o: CMakeFiles/footballgame.dir/flags.make
CMakeFiles/footballgame.dir/draft.c.o: ../draft.c
CMakeFiles/footballgame.dir/draft.c.o: CMakeFiles/footballgame.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/alex/footballsim/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_7) "Building C object CMakeFiles/footballgame.dir/draft.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/footballgame.dir/draft.c.o -MF CMakeFiles/footballgame.dir/draft.c.o.d -o CMakeFiles/footballgame.dir/draft.c.o -c /home/alex/footballsim/draft.c

CMakeFiles/footballgame.dir/draft.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/footballgame.dir/draft.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/alex/footballsim/draft.c > CMakeFiles/footballgame.dir/draft.c.i

CMakeFiles/footballgame.dir/draft.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/footballgame.dir/draft.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/alex/footballsim/draft.c -o CMakeFiles/footballgame.dir/draft.c.s

CMakeFiles/footballgame.dir/league.c.o: CMakeFiles/footballgame.dir/flags.make
CMakeFiles/footballgame.dir/league.c.o: ../league.c
CMakeFiles/footballgame.dir/league.c.o: CMakeFiles/footballgame.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/alex/footballsim/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_8) "Building C object CMakeFiles/footballgame.dir/league.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/footballgame.dir/league.c.o -MF CMakeFiles/footballgame.dir/league.c.o.d -o CMakeFiles/footballgame.dir/league.c.o -c /home/alex/footballsim/league.c

CMakeFiles/footballgame.dir/league.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/footballgame.dir/league.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/alex/footballsim/league.c > CMakeFiles/footballgame.dir/league.c.i

CMakeFiles/footballgame.dir/league.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/footballgame.dir/league.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/alex/footballsim/league.c -o CMakeFiles/footballgame.dir/league.c.s

CMakeFiles/footballgame.dir/main_menu.c.o: CMakeFiles/footballgame.dir/flags.make
CMakeFiles/footballgame.dir/main_menu.c.o: ../main_menu.c
CMakeFiles/footballgame.dir/main_menu.c.o: CMakeFiles/footballgame.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/alex/footballsim/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_9) "Building C object CMakeFiles/footballgame.dir/main_menu.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/footballgame.dir/main_menu.c.o -MF CMakeFiles/footballgame.dir/main_menu.c.o.d -o CMakeFiles/footballgame.dir/main_menu.c.o -c /home/alex/footballsim/main_menu.c

CMakeFiles/footballgame.dir/main_menu.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/footballgame.dir/main_menu.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/alex/footballsim/main_menu.c > CMakeFiles/footballgame.dir/main_menu.c.i

CMakeFiles/footballgame.dir/main_menu.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/footballgame.dir/main_menu.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/alex/footballsim/main_menu.c -o CMakeFiles/footballgame.dir/main_menu.c.s

# Object files for target footballgame
footballgame_OBJECTS = \
"CMakeFiles/footballgame.dir/main.c.o" \
"CMakeFiles/footballgame.dir/coach.c.o" \
"CMakeFiles/footballgame.dir/player.c.o" \
"CMakeFiles/footballgame.dir/team.c.o" \
"CMakeFiles/footballgame.dir/game.c.o" \
"CMakeFiles/footballgame.dir/csv_parser.c.o" \
"CMakeFiles/footballgame.dir/draft.c.o" \
"CMakeFiles/footballgame.dir/league.c.o" \
"CMakeFiles/footballgame.dir/main_menu.c.o"

# External object files for target footballgame
footballgame_EXTERNAL_OBJECTS =

footballgame: CMakeFiles/footballgame.dir/main.c.o
footballgame: CMakeFiles/footballgame.dir/coach.c.o
footballgame: CMakeFiles/footballgame.dir/player.c.o
footballgame: CMakeFiles/footballgame.dir/team.c.o
footballgame: CMakeFiles/footballgame.dir/game.c.o
footballgame: CMakeFiles/footballgame.dir/csv_parser.c.o
footballgame: CMakeFiles/footballgame.dir/draft.c.o
footballgame: CMakeFiles/footballgame.dir/league.c.o
footballgame: CMakeFiles/footballgame.dir/main_menu.c.o
footballgame: CMakeFiles/footballgame.dir/build.make
footballgame: CMakeFiles/footballgame.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/alex/footballsim/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_10) "Linking C executable footballgame"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/footballgame.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/footballgame.dir/build: footballgame
.PHONY : CMakeFiles/footballgame.dir/build

CMakeFiles/footballgame.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/footballgame.dir/cmake_clean.cmake
.PHONY : CMakeFiles/footballgame.dir/clean

CMakeFiles/footballgame.dir/depend:
	cd /home/alex/footballsim/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/alex/footballsim /home/alex/footballsim /home/alex/footballsim/build /home/alex/footballsim/build /home/alex/footballsim/build/CMakeFiles/footballgame.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/footballgame.dir/depend

