cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(intro)

set(CMAKE_PREFIX_PATH $PWD/../../libtorch)
#set(CMAKE_PREFIX_PATH /mnt/d/ANACONDA/envs/Pytorch/lib/site-packages/torch/share/cmake)
#set(CMAKE_PREFIX_PATH /home/hiroforyou/anaconda3/envs/Pytorch/lib/python3.7/site-packages/torch/share/cmake)
find_package(Torch REQUIRED)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${TORCH_CXX_FLAGS}")

add_executable(${PROJECT_NAME} intro.cpp)
target_link_libraries(${PROJECT_NAME} "${TORCH_LIBRARIES}")
set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD 14)
