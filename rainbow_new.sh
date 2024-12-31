#!/bin/sh

# This actually makes your LEDs paint a rainbow; and dims them
# should work on OpenWrt from 23.05

echo 255 0 0 > /sys/class/leds/rgb\:power/multi_intensity
echo 255 115 0 > /sys/class/leds/rgb\:lan-0/multi_intensity
echo 255 234 0 > /sys/class/leds/rgb\:lan-1/multi_intensity
echo 162 255 0 > /sys/class/leds/rgb\:lan-2/multi_intensity
echo 47 255 0 > /sys/class/leds/rgb\:lan-3/multi_intensity
echo 0 255 68 > /sys/class/leds/rgb\:lan-4/multi_intensity
echo 0 255 187 > /sys/class/leds/rgb\:wan/multi_intensity
echo 0 208 255 > /sys/class/leds/rgb\:wlan-1/multi_intensity
echo 0 94 255 > /sys/class/leds/rgb\:wlan-2/multi_intensity
echo 21 0 255 > /sys/class/leds/rgb\:wlan-3/multi_intensity
echo 140 0 255 > /sys/class/leds/rgb\:indicator-1/multi_intensity
echo 255 0 255 > /sys/class/leds/rgb\:indicator-2/multi_intensity
echo 2 > /sys/devices/platform/soc/soc:internal-regs/f1011000.i2c/i2c-0/i2c-1/1-002b/brightness
