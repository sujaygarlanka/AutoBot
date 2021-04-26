# AutoBot (Older Versions)
In this folder is code and details for the older versions of the TennisBot

## v0.0
This version was the RC car that could be controlled via the iPhone.

The overall design was an hArduino controlling the car, a Bluetooth module communicating to the Arduino via the serial ports, and the iPhone sending commands over Bluetooth to the Bluetooth module. 

### Software
 - Code on Arduino found in the `v0/arduino` folder
 - iPhone app found in `v0/ios` folder

### Hardware
#### Parts
- [RC Car - Monster Jam Grave Digger 1:15](https://www.amazon.com/Monster-Jam-Official-Remoter-Control/dp/B07HGR66Q5?pd_rd_w=aHP5k&pf_rd_p=3fdb7f7b-31a2-4f37-b9bc-1469e3d4fb18&pf_rd_r=ST42RDH626Q38TD325DR&pd_rd_r=0108b0e8-8dd8-4746-af2a-839fe3614d4b&pd_rd_wg=Fw5vf)
- [Motor Controller - l298n](https://www.amazon.com/Controller-Module-Bridge-Stepper-Arduino/dp/B07RB2LWD7/ref=sr_1_2?crid=1CMZ5QN0DK2FH&dchild=1&keywords=l298n&qid=1602009931&sprefix=l298%2Ctoys-and-games%2C141&sr=8-2)
- [Bluetooth transceiver (Connects to iPhone)](https://www.amazon.com/gp/product/B06WGZB2N4/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
- [Batteries](https://www.amazon.com/gp/product/B083K4XSKG/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1)
- [Battery holder](https://www.amazon.com/gp/product/B0858WTZM7/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)
- [Switches](https://www.amazon.com/5Pcs-Rocker-Switch-Position-QTEATAK/dp/B07Y1GDRQG/ref=sr_1_6?dchild=1&keywords=electronic+switch&qid=1602948480&sr=8-6)

### Resources
#### Bluetooth
- Guides for Bluetooth connection between iPhone and HM-10
    - http://www.hangar42.nl/hm10
    - https://www.freecodecamp.org/news/ultimate-how-to-bluetooth-swift-with-hardware-in-20-minutes/
- Bluetooth commands: https://drive.google.com/file/d/17Zf_pb6ikwaUtI67UDObh17c07OQFQOh/view

## v1.0
This version was the RC car that could be controlled over Wifi by a computer on the same network as the car.

The overall design was an Raspberry Pi controlling the car that could connect over Wifi to a python server on a computer on the same network that would send it commands.

### Software
 - Code on Raspberry Pi found in the `v1/raspberry_pi` folder
 - Python server code found at `v1/server.py`

### Hardware
#### Parts
- [RC Car - Monster Jam Grave Digger 1:15](https://www.amazon.com/Monster-Jam-Official-Remoter-Control/dp/B07HGR66Q5?pd_rd_w=aHP5k&pf_rd_p=3fdb7f7b-31a2-4f37-b9bc-1469e3d4fb18&pf_rd_r=ST42RDH626Q38TD325DR&pd_rd_r=0108b0e8-8dd8-4746-af2a-839fe3614d4b&pd_rd_wg=Fw5vf)
- [Motor Controller - l298n](https://www.amazon.com/Controller-Module-Bridge-Stepper-Arduino/dp/B07RB2LWD7/ref=sr_1_2?crid=1CMZ5QN0DK2FH&dchild=1&keywords=l298n&qid=1602009931&sprefix=l298%2Ctoys-and-games%2C141&sr=8-2)
- [Raspberry Pi Zero Wireless](https://www.amazon.com/CanaKit-Raspberry-Wireless-Complete-Starter/dp/B072N3X39J/ref=sr_1_3?dchild=1&keywords=raspberry+pi+zero+wireless&qid=1619133746&sr=8-3)
- [Batteries](https://www.amazon.com/gp/product/B083K4XSKG/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1)
- [Battery holder](https://www.amazon.com/gp/product/B0858WTZM7/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)
- [Switches](https://www.amazon.com/5Pcs-Rocker-Switch-Position-QTEATAK/dp/B07Y1GDRQG/ref=sr_1_6?dchild=1&keywords=electronic+switch&qid=1602948480&sr=8-6)

### Resources
- Guidance on how to setup Raspberry Pi: https://github.com/sujaygarlanka/DrinkMixr-Raspberry-Pi




