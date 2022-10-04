# Autonomous Bot

### Shows controls and basic object detection. Working on simplified autonomous navigation.

<img src="https://raw.githubusercontent.com/sujaygarlanka/AutoBot/main/media/demo_gif.gif" width="50%" />

Full video demo here: 

https://user-images.githubusercontent.com/21188938/117176844-53f5fc80-ad9e-11eb-9bf9-94ac9eb4bc4e.mov

# Introduction
The OpenBot open-source project started by Vladlen Koltun, former Chief Scientist of Intelligent Systems at Intel, provides the blueprint and software to create an inexpensive 3D-printed robot that leverages the smartphone as the brains. Inspired by this, I created my own software, hardware and chassis for a robot. My progress on this is shown below.

# Design

The overall design is to situate a cheap phone on the robot to wirelessly send visual information to a computer that will then process that information and send the appropriate command wirelessly to the bot, thus creating a closed loop system with visual feedback as shown above. The design depends on the computer, phone and robot being on the same Wifi network because Wifi is used for wireless communication. A downside of this is some latency as well as being constrained to the physical area of the Wifi network. However, the benefits include allowing for scalable compute power, the ability to take advantage of desktop/server ML frameworks like PyTorch and Tensorflow with their large open-source communities and having a flexible coding environment that will allow for easy and powerful experimenting. Before this, the initial prototype had computation localized to the robot by having an iPhone situated on the robot that took in a visual feed, performed some computation and send commands over Bluetooth to the robot akin to the architecture of OpenBot. However, the mobile platform employing computer vision for perception proved problematic in quickly iterating. In addition, slow compile times and difficulties that arise from mobile programming made this first version a sub optimal platform for experimenting.![image](https://user-images.githubusercontent.com/21188938/193909506-407f6435-310b-4d02-b1a9-14c37f4ce7fc.png)

# Components

The important components of the robot platform are the phone/camera, the chassis, the electronic hardware in the chassis and finally the software stack processing visual input and sending commands to the robot.

Smartphone/Camera:
For visual input, the only thing needed is a Wifi enabled camera. The Wifi enabled camera used is an inexpensive Android smartphone. This could not be used to run the robot, but it would be enough to stream a camera feed to the internet. I used an app called IPWebcam that set the phone up as a server on the local area network from which the camera feed could be accessed.

Chassis:
The chassis for the robotic platform is a retrofitted RC car. This obviates the need for a 3D printer. In addition, the RC car uses rack-and-pinion steering as used in automobiles instead of differential steering used in vehicles like OpenBot and tanks. Experimenting on a platform with rack-and-pinion steering is more difficult, but also far more enticing because it mimics how real cars operate. This allows experimenting with self-driving on a far smaller scale. Also, the chassis has a camera holder that can change the camera viewing angle of the phone by using a servo to reduce or increase the length of a supporting string that maps to a specific camera tilt as shown below.


# Architecture
All components are connected to the same Wifi network.
- Phone
  - Android phone runs [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en_US&gl=US) which streams video to a local IP on the Wifi network. 
- Computer
  - Then the computer running the code in `server/main.py`, pulls the video stream from the localIP and can use it to localize the car, detect objects around or anything else to inform how to move the car. Then the computer can send commands over a tcp socket connection to the car.
- Car
  - The car receives commands the tcp socket connection to move forward, backward, left and right and how much to tilt the camera. Hardware for the car can be found in the [Hardware](#hardware) section

# Software
- Phone 
  - [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en_US&gl=US)
- Computer
  - Runs code in `server/main.py`
- Car
  - Runs code found here https://go.particle.io/shared_apps/6086451d4c3ada0009ff0181.

# Hardware

## Phone
Any Android phone

## Computer
Any computer that can run python

## Car

### Parts
- [RC Car - Monster Jam Grave Digger 1:15](https://www.amazon.com/Monster-Jam-Official-Remoter-Control/dp/B07HGR66Q5?pd_rd_w=aHP5k&pf_rd_p=3fdb7f7b-31a2-4f37-b9bc-1469e3d4fb18&pf_rd_r=ST42RDH626Q38TD325DR&pd_rd_r=0108b0e8-8dd8-4746-af2a-839fe3614d4b&pd_rd_wg=Fw5vf)
- [Motor Controller - l298n](https://www.amazon.com/Controller-Module-Bridge-Stepper-Arduino/dp/B07RB2LWD7/ref=sr_1_2?crid=1CMZ5QN0DK2FH&dchild=1&keywords=l298n&qid=1602009931&sprefix=l298%2Ctoys-and-games%2C141&sr=8-2)
- [Argon Wifi Development Board](https://store.particle.io/products/argon)
- [Batteries](https://www.amazon.com/gp/product/B083K4XSKG/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1)
- [Battery holder](https://www.amazon.com/gp/product/B0858WTZM7/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)
- [Switches](https://www.amazon.com/5Pcs-Rocker-Switch-Position-QTEATAK/dp/B07Y1GDRQG/ref=sr_1_6?dchild=1&keywords=electronic+switch&qid=1602948480&sr=8-6)

### Measurements
Ranges were calculating by applying no resistance and full resistance to the motors.

| Item         | Voltage Range (V)| Amp Range (A)|       
| -----------  | ---------------- | ------------ |
| Front Motor  | 5.3 - 5.3        | 0.85 - 0.85  |
| Rear Motor   | 4.5 - 6.5        | 0.25 - 2.6   |
