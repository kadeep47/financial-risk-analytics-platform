cmake_minimum_required(VERSION 3.10)
project(CashflowEngine)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Threading
find_package(Threads REQUIRED)

file(GLOB SOURCES "src/*.cpp")

add_executable(engine ${SOURCES})
target_link_libraries(engine PRIVATE Threads::Threads)
