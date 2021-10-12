#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
from smbus import SMBus

color_names = {"white": 0xFFFFFF, "black": 0x000000, "red": 0xFF0000, "green": 0x00FF00, "blue": 0x0000FF, "yellow": 0xFFFF00, "violet": 0xFF00FF, "cyan": 0x00FFFF, "orange": 0xFF8000, "pink": 0xFF0080}

valid_leds = {"pwr": 11, "lan0": 10, "lan1": 9, "lan2": 8, "lan3": 7, "lan4": 6, "wan": 5, "pci1": 4, "pci2": 3, "pci3": 2, "usr1": 1, "usr2": 0, "all": -1, "lan": -2}

bus = SMBus(1)
i2c_addr = 0x2A

def main() -> int:
    if len(sys.argv) < 2:
        show_usage()
        return 0
    commands = parse_args(sys.argv[1:])
    for cmd in commands:
        which_leds = []
        if "dev" in cmd:
            if cmd["dev"] == "all":
                which_leds = list(valid_leds.values())
                which_leds.remove(-1)
                which_leds.remove(-2)
            elif cmd["dev"] == "lan":
                for key, val in valid_leds.items():
                    if key.startswith("lan"):
                        which_leds.append(val)
                which_leds.remove(-2)
            else:
                which_leds = [valid_leds[cmd["dev"]]]
        if "color" in cmd:
            if cmd["color"] in color_names:
                cmd["color"] = color_names[cmd["color"]]
            else:
                cmd["color"] = int(cmd["color"], 16)
            col_R = (cmd["color"] & 0xFF0000) >> 16
            col_G = (cmd["color"] & 0x00FF00) >> 8
            col_B = (cmd["color"] & 0x0000FF)
            i2c_col_cmd = [ col_R, col_G, col_B ]
            for led in which_leds:
                bus.write_i2c_block_data(i2c_addr, 5, [led] + i2c_col_cmd)
        if "status" in cmd:
            if cmd["status"] == "auto":
                i2c_mode = 0x00
            elif cmd["status"] == "enable":
                i2c_mode = 0x10
                i2c_state = 0x10
            else:
                i2c_mode = 0x10
                i2c_state = 0x00
            for led in which_leds:
                bus.write_byte_data(i2c_addr, 3, i2c_mode | led)
                if cmd["status"] != "auto":
                    bus.write_byte_data(i2c_addr, 4, i2c_state | led)
        if "keyword" in cmd:
            if cmd["keyword"] == "intensity":
                bus.write_byte_data(i2c_addr, 7, cmd["value"])
            elif cmd["keyword"] == "binmask":
                x = 0
                while x < 12:
                    if cmd["value"] >> x & 1:
                        bus.write_byte_data(i2c_addr, 4, 0x10 | x)
                    else:
                        bus.write_byte_data(i2c_addr, 4, 0x00 | x)
                    x += 1
            elif cmd["keyword"] == "get":
                if cmd["value"] == "intensity":
                    print("Intensity: {}".format(bus.read_byte_data(i2c_addr, 8)))
    return 0

def parse_args(argv):
    command_list = []
    current_command = {}
    run_keyword = False
    for param in argv:
        if run_keyword != False:
            try:
                if run_keyword == "intensity":
                    current_command["value"] = int(param)
                elif run_keyword == "binmask":
                    current_command["value"] = int(param, 16)
                else:
                    current_command["value"] = param
            except:
                raise ValueError("Bad value: not an int", param)
            run_keyword = False
        elif is_keyword(param) == True:
            if len(current_command) > 0:
                command_list.append(current_command)
                current_command = {}
            run_keyword = param
            current_command = {"keyword": param}
        elif is_led(param) == True:
            if len(current_command) > 0:
                command_list.append(current_command)
                current_command = {}
            current_command = {"dev": param}
        elif is_color(param) == True:
            current_command["color"] = param
        elif is_status(param) == True:
            current_command["status"] = param
        else:
            raise ValueError("Bad option", param)
    if run_keyword != False:
        raise ValueError("Bad option: missing value", param)
    command_list.append(current_command)
    return command_list

def is_led(param):
    if param in valid_leds:
        return True
    return False

def is_color(param):
    if param in color_names:
        return True
    if re.match("^[0-9A-Fa-f]{6}$", param):
        return True
    return False

def is_status(param):
    valid_status = ["enable", "disable", "auto"]
    if param in valid_status:
        return True
    return False

def is_keyword(param):
    keywords = ["intensity", "binmask", "get"]
    if param in keywords:
        return True
    return False

def show_usage():
    usage = """Usage:
\tSet devices: rainbow.py DEV_CONFIGURATION [DEV_CONFIGURATION ...]

DEV_CONFIGURATION is one of the next options:
DEV COLOR STATUS or DEV STATUS COLOR or DEV STATUS or DEV COLOR, where:
\tDEV:\t'pwr' (power LED),
\t\t'lan0', 'lan1', 'lan2', 'lan3', 'lan4' (LAN port LEDs),
\t\t'wan' (WAN port LED),
\t\t'pci1', 'pci2', 'pci3' (PCI LEDs),
\t\t'usr1', 'usr2' (user-defined LEDs),
\t\tor alias 'all' for all previous LEDs,
\t\t\t'lan' for all LAN port LEDs
\tCOLOR: name of predefined color (red, blue, green, white, black = off, yellow, violet, cyan, orange, pink)
\t\tor 3 bytes for RGB, so red is 'FF0000', green is '00FF00', blue is '0000FF' etc.
\tSTATUS: 'enable' (LED is always on), 'disable' (LED is always OFF)
\t\t'auto' (LED shows HW activity, i.e. flashing)

'intensity' PERCENTAGE, where:
\tPERCENTAGE is a number between 0 to 100 (percent of maximum brightness).

'binmask' MASK:
\tUse MASK (hexadecimal) as mask to set ENABLE/DISABLE
\tstatus of LEDs. MSB is PWR LED and LSB is USR2. Max value is 0xFFF = all LEDs on.

'get' VALUE, where:
\tVALUE is 'intensity' (returns intensity of LEDs as set above)
\t(no more getters are available for now)

Examples:
rainbow.py all blue auto - reset status of all LEDs and set their color to blue
rainbow.py all blue pwr red - set color of all LEDs to blue except Power LED (red)
rainbow.py all enable wan auto - all LEDs will be always on except the LED of WAN port
\t\t\t\tthat will flash according to traffic"""
    print(usage)

if __name__ == '__main__':
    sys.exit(main())
