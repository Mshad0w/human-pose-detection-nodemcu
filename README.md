# human-pose-detection-nodemcu
Using Mediapipe python library in order to body pose detection and making a http request to an esp8266 nodemcu server for home/office automation purpose

-In Pose Detection.py file you can change camera address as video processing source,in this case,it is a RTSP home camera URL

-It detects a gesture when you raise your both hand within an angle between 75-105 degree in front of camera using python mediapipe library

-Then it sends an http POST data request to listening Nodemcu server on defined IP/Port (192.168.1.20,8888) by a message of "hello buddy" phrase,

-The Nodemcu http server will send a command code with RCSwitch library to a remote relay or Device after receiving "hello buddy" from local python camera processing server.
