# PiMidiClock
Raspberry Pi project that reads MIDI clock tempo and displays it on a Unicorn HAT HD LED matrix

This blog post dives deeper into a Raspberry Pi project that reads MIDI clock tempo and displays it on a Unicorn HAT HD LED matrix. Inspired by the lack of a tempo display on the Behringer RD-78, this DIY solution uses Python to visualize BPM in real time.

Why This Project?

Many drum machines and synths—like the RD-78—don’t show the current tempo, making it hard to sync gear precisely. This project solves that by using a Raspberry Pi to read MIDI clock pulses and display the BPM on a compact LED matrix.

**Hardware Used**
Raspberry Pi 4 (any model with USB will work)
Unicorn HAT HD LED matrix
USB MIDI Interface (tested with a £14 model)
SD card with Raspberry Pi OS
Power supply and cables
Software Setup
Install Raspberry Pi OS: Download from the official site and flash to your SD card.
Python Environment: Use built-in Python 3 and install required libraries:

pip install unicornhathd mido python-rtmidi
Python Script:

Reads MIDI clock pulses via USB
Calculates BPM from pulse timing
Displays BPM on Unicorn HAT HD
Includes font rendering and smoothing logic
