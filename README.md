# Foosbot
Auto scoring foosball bot for raspberry pi

Using python 2.7 on Raspbian OS (Linux) 4.1.6-v7+

Directory Structure:
The directory structure is standard for a web.py app
bin - app.py The main application - from the containing directory run with ```sudo python bin/app.py```
docs - documentation
foosbot - internal directory for ```__init__()```
templates - all the html templates that are referrenced from app.py
tests - for any unit tests

The GPIO mapping is:
21 - hardware reset button
20 - break-beam IR sensor
26 - break-beam IR sensor

I used the following components:
Raspberry Pi with wifi. I used a Pi 2 B+ with an external wifi adapter, but the Pi 3 has wifi and bluetooth built in, so I'd recommend it. There is a starter pack on AdaFruit that comes with the Pi 3 and lots of handy accessories: https://www.adafruit.com/products/3058

The power supply is required. The breadboard, jumper wires, buttons, and LEDs are very handy for prototyping your projects.

2 IR break beam sensors. We used these 3mm sensors from AdaFruit: https://www.adafruit.com/products/2167

1 button for resetting an unfinished game. You could probably do it in software, but I had some buttons laying around and hardware buttons are nice, especially if something goes wrong :)

Input and display. You can use any USB keyboard/mouse and HDMI monitor. For this project we used a small, Pi-mountable touchscreen: https://www.adafruit.com/products/1601

If I were doing it again, I would use this larger, higher-res touchscreen:
https://www.adafruit.com/products/2097
