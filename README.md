# AutoBot

# Demo of Current Version
### Simply shows controls and basic object detection
https://user-images.githubusercontent.com/21188938/117176844-53f5fc80-ad9e-11eb-9bf9-94ac9eb4bc4e.mov

# Architecture
All components are connected to the same Wifi network.

Components
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

## Resources
