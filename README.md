# pymarash
A Python bridge between the MAplin Robotic Arm and ScratcH (pyMarash)

This is an extension for the off-line version of Scratch, developed
in one hour so very likely to be buggy etc.
I have tested it with Scratch 2.0 on a MacBook running Mac OS X 10.11,
it should run without problems on a Linux, including a Raspberry Pi.

Quick installation instructions:
- Install pyUSB with pip install --pre pyusb
- Install libusb (I have used Homebrew, with brew install libusb)
- Launch with python pymarash_http_server.py
- Start Scratch, while pressing the SHIFT key click on File, select Import experimental HTTP Extension, browse to the location of the file ScratchArm.json and select it.

I used material from the following sources:
- https://github.com/MrYsLab/s2a_fm/ (an example of Python extension for
  off-line Scratch)
- http://notbrainsurgery.livejournal.com/38622.html (description of the USB protocol)
- http://www.wikihow.com/Use-a-USB-Robotic-Arm-with-a-Raspberry-Pi-%28Maplin%29 (just for the python example)
- https://armctrl.codeplex.com/ (XCode project if you are interested in a C implementation)
