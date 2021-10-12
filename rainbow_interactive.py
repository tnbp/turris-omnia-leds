#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from smbus import SMBus
import sys
import os
import re

clear = lambda: os.system('clear')

led_ids = {"0": "USER_LED2", "1": "USER_LED1", "2": "PCI3_LED",
           "3": "PCI2_LED", "4": "PCI1_LED", "5": "WAN_LED",
           "6": "LAN4_LED", "7": "LAN3_LED", "8": "LAN2_LED",
           "9": "LAN1_LED", "10": "LAN0_LED", "11": "PWR_LED"}

bus = SMBus(1)
i2c_addr = 0x2A

def main() -> int:
    cmd_input = ""
    led_input = ""
    i2c_reg = -1
    i2c_cmd = []
    for i in range(3):
        for j in range(4):
            cur = 4*i+j
            print(str(cur) + ": " + led_ids[str(cur)] + "\t", end="")
        print()
    while led_input not in led_ids:
        led_input = input("Enter a LED number [0-11]: ")
    led_num = int(led_input)
    print("\n:: SELECTED LED ID " + str(led_num) + " (" + led_ids[str(led_num)] + ") ::\n")
    print("1: Turn LED on")
    print("2: Turn LED off")
    print("3: Change LED color")
    print("4: Change ALL LED brightness\n")
    while cmd_input not in ["1", "2", "3", "4"]:
        cmd_input = input("Enter a command [1-4]: ")
    clear()
    if cmd_input == "1":
        print("Sending I2C command: SET USER MODE")
        i2c_reg = 3
        i2c_cmd = 0x10
        i2c_cmd |= led_num
        print("::\twrite_byte_data(0x{:02X}, {}, 0x{:02X})".format(i2c_addr, str(i2c_reg), i2c_cmd))
        bus.write_byte_data(i2c_addr, i2c_reg, i2c_cmd)
        print("Sending I2C command: TURN LED ON")
        i2c_reg = 4
        i2c_cmd = 0x10
        i2c_cmd |= led_num
        print("::\twrite_byte_data(0x{:02X}, {}, 0x{:02X})".format(i2c_addr, str(i2c_reg), i2c_cmd))
        bus.write_byte_data(i2c_addr, i2c_reg, i2c_cmd)
    elif cmd_input == "2":
        print("Sending I2C command: SET USER MODE")
        i2c_reg = 3
        i2c_cmd = 0x10
        i2c_cmd |= led_num
        print("::\twrite_byte_data(0x{:02X}, {}, 0x{:02X})".format(i2c_addr, str(i2c_reg), i2c_cmd))
        bus.write_byte_data(i2c_addr, i2c_reg, i2c_cmd)
        print("Sending I2C command: TURN LED OFF")
        i2c_reg = 4
        i2c_cmd = 0x00
        i2c_cmd |= led_num
        print("::\twrite_byte_data(0x{:02X}, {}, 0x{:02X})".format(i2c_addr, str(i2c_reg), i2c_cmd))
        bus.write_byte_data(i2c_addr, i2c_reg, i2c_cmd)
    elif cmd_input == "3":
        print("Sending I2C command: SET USER MODE")
        i2c_reg = 3
        i2c_cmd = 0x10
        i2c_cmd |= led_num
        print("::\twrite_byte_data(0x{:02X}, {}, 0x{:02X})".format(i2c_addr, str(i2c_reg), i2c_cmd))
        bus.write_byte_data(i2c_addr, i2c_reg, i2c_cmd)
        led_col = ""
        led_col_valid = False
        while led_col_valid == False:
            led_col = input("Enter desired LED color (RRGGBB): 0x")
            if re.match("^[0-9A-Fa-f]{6}$", led_col):
                led_col_valid = True
                print("Valid color: {}".format(led_col))#
            led_col_R = int(led_col[0:2], 16)
            led_col_G = int(led_col[2:4], 16)
            led_col_B = int(led_col[4:6], 16)
        print("Sending I2C command: CHANGE LED COLOR")
        i2c_reg = 5
        i2c_cmd = [ led_num ]
        i2c_col_cmd = [ led_col_R, led_col_G, led_col_B ]
        i2c_cmd += i2c_col_cmd
        print("::\twrite_i2c_block_data(0x{:02X}, {}, [{}])".format(i2c_addr, str(i2c_reg), ", ".join("0x{:02X}".format(e) for e in i2c_cmd)))
        bus.write_i2c_block_data(i2c_addr, i2c_reg, i2c_cmd)
    elif cmd_input == "4":
        print("Sending I2C command: SET USER MODE")
        i2c_reg = 3
        i2c_cmd = 0x10
        i2c_cmd |= led_num
        print("::\twrite_byte_data(0x{:02X}, {}, 0x{:02X})".format(i2c_addr, str(i2c_reg), i2c_cmd))
        bus.write_byte_data(i2c_addr, i2c_reg, i2c_cmd)
        led_bns = -1
        led_bns_valid = False
        while led_bns_valid == False:
            try:
                led_bns = int(input("Enter desired LED brightness:     %\b\b\b\b\b"))
                if led_bns >= 0 and led_bns <= 100:
                    led_bns_valid = True
            except:
                print("LOL NOPE")
        print("Sending I2C command: CHANGE LED BRIGHTNESS")
        i2c_reg = 7
        i2c_cmd = led_bns
        print("::\twrite_byte_data(0x{:02X}, {}, 0x{:02X})".format(i2c_addr, str(i2c_reg), led_bns))
        bus.write_byte_data(i2c_addr, i2c_reg, i2c_cmd)

    print("\n")
    return main()
    
if __name__ == '__main__':
    sys.exit(main())
