# MA4822

This was developed for the MA4822, Measurement and Sensing systems in NTU, Singapore. The scope of the project is to build 
a measurement and sensing system for an autonomous sea surface vehicle. 
An arduino-raspberry pi based system was designed as a prototype for the measurement system to monitor the temperature, depth 
to surface, humidity, wind speed and wind direction. The measurements made by the arduino are sent via USB serial to the 
rapsberry pi 3 model B. A webcam is connected to the raspberry pi, which perfroms image processing to identify colored shapes 
in the environment. The video stream is then sent over a server to be viewed from the ground station. 
In addition a ROS-Gazebo simulation was also developed to test the concept of mapping and autonomous obstacle avoidance. 
The packages for the ROS simulation will be uploaded soon. 
