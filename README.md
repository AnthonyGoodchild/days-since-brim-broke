# Days Since Brim Broke
Physical day counter for the important stat of days since brim broke. 

## Hardware

- InkyPHAT (pimoroni)
- Raspberry Pi Zero
- CJE Realtime Clock (http://www.cjemicros.co.uk/micros/products/rpirtc.shtml)
- Momentary push button switch

### Pinouts

InkyPHAT pinout can be wired using 6 GPIO pins; hardware pins 11, 13, 15, 19, 23 & 24, plus two power and one ground pin.

https://pinout.xyz/pinout/inky_phat

The CJE RTC is wired on I2C, pins 3 & 5, plus 3v3, 5v and ground. It does not conflict with any InkyPHAT pins required, and can share both 3v3/5v pins.

The momentary switch is directly wired between ground and GPIO 1 (HW pin 28) which is protected by a 1.8k pull-up resistor internally.


## Software

- Python 3
- Inky Phython Library (https://github.com/pimoroni/inky)

hwclock was set up using dtoverlay for `ds1307`, written back to software clock in `rc.local` with `hwclock -s`.

### Installation

```pip3 install -r requirements.txt```

run at boot from `/etc/rc.local` with 

```python3 /home/pi/days-since-brim-broke/brim.py &```

(before call to exit)