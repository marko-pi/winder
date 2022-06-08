# Software for a simple motor winding machine

This is a really simple program for a small DC winding machine. You can see the motivation for creating a motor winding machine and its operation in this [video](https://youtu.be/0TUpQcnt1OU). You can read discussion on this topic [here](https://forum.mrhmag.com/post/customization-of-small-dc-motors-12365024).

## Schematics for the winding machine:

![winder](https://user-images.githubusercontent.com/18025812/172726742-219effce-725a-4143-96c7-33813451a02d.png)

## Basic explanation of the program:

The heart of the setup is continuous servo motor. Library **pigpio** has a pulsewidth range between 1000 and 2000, with 1000 representing fastest (0.58 Hz) clockwise rotation, 1500 a standstill and 2000 fastest (0.58 Hz) counter-clockwise rotation.  Unfortunatelly, the speed is not linearly proportional to the pulsewidth.  I experimentally determined the pulsewidths for 0.5 Hz, 0.4 Hz, 0.3 Hz and 0.2 Hz, which are saved in list **serv**.  You might have to determine and correct those values for your servo motor yourself.

The setup uses MAX7219 controlled 8 number 7 segment display.  The program already contains all necessary code for communication with MAX7219.  In particular, function **mwri(num, pos, siz)** displays number **num** at position **pos** with minimum length of **siz**. List **mnum** contains the information on which segments must be displayed for each number and minus sign.
