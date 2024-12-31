# turris-omnia-leds
Lets you control the LEDs of your Turris Omnia, **even on vanilla OpenWrt**.

### NOTE: As both OpenWrt 23.05 and 24.10 seem to include kernel drivers for these LEDs now, this script will not work on newer releases (`Resource busy`).
LEDs can now be controlled by `echo`ing values into `/sys/class/leds/rgb:*`, rendering these scripts obsolete.

This is a replacement for Turris OS's "rainbow" script which lets you control the status, color and brightness of your Turris Omnia's LEDs.

Unlike most other scripts I have seen so far, **this one does not require the original CZ.NIC firmware**, i.e. it **works with vanilla OpenWrt**. Dependencies are ``python3`` and ``python3-smbus``, please install from opkg/LuCI.

Relevant hardware description here: https://gitlab.nic.cz/turris/hw/omnia_hw_ctrl/-/blob/master/turris_omnia_i2c_desc.adoc
