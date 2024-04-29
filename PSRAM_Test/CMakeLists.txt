cmake_minimum_required(VERSION 3.16)

set(SDKCONFIG_DEFAULTS "${CMAKE_CURRENT_LIST_DIR}/main/sdkconfig")
set(SDKCONFIG "${CMAKE_CURRENT_LIST_DIR}/build/sdkconfig")

# bring in ESP-IDF build system functions and macros
include($ENV{IDF_PATH}/tools/cmake/project.cmake)

if(NOT DEFINED VERSION_CODE)
set(VERSION_CODE "build_test")
endif()

add_compile_definitions(VERSION_CODE="${VERSION_CODE}")

include_directories(${CMAKE_CURRENT_LIST_DIR}/main/inc)

include(${CMAKE_CURRENT_LIST_DIR}/main/project.cmake)

project(${MODEL_NUMBER})
