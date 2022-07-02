#!/bin/sh

# This actually makes your LEDs paint a rainbow; and dims them
./rainbow.py pwr ff0000 lan0 ff7300 lan1 ffea00 lan2 a2ff00 lan3 2fff00 lan4 00ff44 wan 00ffbb pci1 00d0ff pci2 005eff pci3 1500ff usr1 8c00ff enable usr2 ff00ff enable
./rainbow.py intensity 2
