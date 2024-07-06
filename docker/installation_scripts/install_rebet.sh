#!/bin/bash

# variables for the installation
export pkg_dir=/home/ubuntu/rebet_ws

mkdir -p $pkg_dir/src/

# Update the package list
sudo apt-get update
sudo apt-get upgrade -y


sudo apt -y install ros-humble-navigation2
sudo apt -y install ros-humble-nav2-bringup

pip install ultralytics
pip install masced_bandits

cd $pkg_dir

git clone -b ACSOS https://github.com/EGAlberts/ReBeT.git

mv ReBeT/* .

rm -rf ReBeT/

mv rebet_sim src/
mv rebet src/
mv rebet_msgs src/

cd src

vcs import < rebet/rebet.rosinstall

wget -O BTCPP.zip https://github.com/BehaviorTree/BehaviorTree.CPP/archive/refs/tags/4.1.1.zip
unzip BTCPP.zip
rm BTCPP.zip

cd $pkg_dir 
rosdep install --from-paths src --ignore-src -r -y


source /opt/ros/humble/setup.bash

# Compile the code
colcon build --packages-skip rebet
source install/setup.bash
colcon build --packages-select rebet

echo "export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/home/ubuntu/rebet_ws/install/rebet_sim/share/rebet_sim/models/" >> /home/ubuntu/.bashrc

echo "source $pkg_dir/install/setup.bash" >> /home/ubuntu/.bashrc
source /home/ubuntu/.bashrc
