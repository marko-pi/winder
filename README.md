# Software for a simple motor winding machine

This is a really simple program for a small DC winding machine. You can see the motivation for creating a motor winding machine and its operation in this [video](https://youtu.be/0TUpQcnt1OU). You can read discussion on this topic [here](https://forum.mrhmag.com/post/customization-of-small-dc-motors-12365024).

## Schematics for the winding machine:

![winder](https://user-images.githubusercontent.com/18025812/172726742-219effce-725a-4143-96c7-33813451a02d.png)

## Basic explanation of the program:

The heart of the setup is a continuous servo motor. Library **pigpio** has a pulsewidth range between 1000 and 2000, with 1000 representing fastest (0.58 Hz) clockwise rotation, 1500 a standstill and 2000 fastest (0.58 Hz) counter-clockwise rotation.  Unfortunatelly, the speed is not linearly proportional to the pulsewidth.  I experimentally determined the pulsewidths for 0.5 Hz, 0.4 Hz, 0.3 Hz and 0.2 Hz, which are saved in list **serv**.  You might have to determine and correct those values for your servo motor yourself.

The servo motor is controlled by two push buttons, one increasing speed and one decreasing speed.  If both buttons are pressed at the same moment, the servo motor is stopped. The third button resets the counter.

Number of turns is measured using a magnet and a *linear* hall detector.  When magnet is far from the sensor, the output voltage is approximatelly 1.5V, and when it is near the sensor, that voltage either rises or drops significantly, depending on the magnet orientation. For a correct orientation of the magnet, the digital GPIO will register the presence of the magnet as a change in the state.

The setup uses MAX7219 controlled 8-number 7-segment display to show servo motor speed (values from -5 to 5) and number of turns.  The program already contains all necessary code for communication with MAX7219.  In particular, function **mwri(num, pos, siz)** displays number **num** at position **pos** with minimum length of **siz**. List **mnum** contains the information on which segments must be displayed for each number and minus sign. In principle, MAX7219 is 5V device, but 3.3V GPIO pins usually control it without any problem.
