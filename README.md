# Software for a simple motor winding machine

This is a really simple program for a small DC winding machine. You can see the motivation for creating a motor winding machine and its operation in this [video](https://youtu.be/0TUpQcnt1OU). You can a read discussion on this topic [here](https://forum.mrhmag.com/post/customization-of-small-dc-motors-12365024).

## Circuit diagram for the winding machine:

![winder](https://user-images.githubusercontent.com/18025812/172836431-235539c4-483f-41a5-9025-f2d3fb3eab5d.png)

## Basic explanation of the program:

The heart of the setup is a continuous servo motor. Library **pigpio** has a pulse width range between 1000 and 2000, where 1000 represents the fastest (0.58 Hz) clockwise rotation, 1500 represents a standstill, and 2000 represents the fastest (0.58 Hz) counterclockwise rotation.  Unfortunately, the speed is not linearly proportional to the pulse width.  I experimentally determined the pulse widths for 0.5 Hz, 0.4 Hz, 0.3 Hz and 0.2 Hz, which are saved in list **serv**.  You may have to determine and correct these values for your servo motor yourself.

The servo motor is controlled by two push buttons, one to increase the speed and one to decrease the speed.  When both push buttons are pressed at the same moment, the servo motor is stopped. The third button resets the counter.

The number of turns is measured with a magnet and a *linear* Hall detector.  When the magnet is far from the sensor, the output voltage is about 1.5 V, and when it is close to the sensor, the voltage increases or decreases significantly, depending on the orientation of the magnet. When the magnet is correctly oriented, the digital GPIO registers the presence of the magnet as a change in state.

The setup uses a MAX7219-controlled 8-digit 7-segment LED display to indicate the servo motor speed (values from -5 to 5) and the number of turns.  The program already contains all the necessary code for communication with MAX7219.  In particular, the function **mwri(num, pos, siz)** displays the number **num** at the position **pos** with a minimum length of **siz**. The list **mnum** contains the information which segments must be displayed for each digit and minus sign. In principle, MAX7219 is a 5 V device, but 3.3V GPIO pins usually control it without problems.
