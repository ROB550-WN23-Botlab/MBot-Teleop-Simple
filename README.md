# Overview

This is a teleop program for the MBot with a Pico board microcontroller. 

Arrow keys - drive the robot

q - quits program

## Prerequisites
You will have to ensure that the camera is working in order to get the **full** experience of teleoperating into the MBot.

To ensure that you have access to the camera, you can enable Legacy Camera on the Pi through typing `sudo raspi-config` on the terminal on the Pi and completing the following steps:
1. Go to `3. Interface Options`
2. Go to `I1 Legacy Camera`
3. Select the option to enable camera

Additionally, ensure that the channel `/dev/video0` is an open port on your device by simply entering the command `ls /dev/video0`.

## Usage

You will have to connect to the Raspberry Pi through **three** terminals, each running a different program, in order to run this program. 


1. The **first** terminal window that connects to the Raspberry Pi should run the *shim* binary, which allows the Pico and Raspberry Pi to send messages through LCM. Run this through `botlab-w23`

```bash
./pico_shim
```

2. The **second** terminal window that connects to the Raspberry Pi should run the *timesync* binary. Similarly, run this with `botlab-w23`

```bash
./timesync
```

3. 

**THIS SCRIPT WILL CAUSE THE ROBOT TO MOVE!** Please place something under the base of the robot so it will not move when the wheels turn as you are getting used to the setup. 

The **third** terminal will run the *teleop_simple.py* script. For the functionality of this script, you must allow for X11 forwarding on the connection. For terminal, this means adding an argument: **ssh -X pi@...**

```bash
cd python
python3 teleop_simple.py
```

The arrow keys can now control the robot

