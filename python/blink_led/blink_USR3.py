#!/usr/bin/env python3
"""
Blink USR3 LED at 5 Hz
This Python program blinks the USR3 LED on a BeagleBone at a frequency of 5 Hz.
It uses the Adafruit_BBIO library to control the GPIO pins.
Author: JJ Tellez
License: MIT License
"""

import time
import Adafruit_BBIO.GPIO as GPIO

def blink_usr3_led(frequency_hz):
    """
    Blinks the USR3 LED at the specified frequency in Hz.
    Args:
        frequency_hz (float): Blink frequency recorded in Hertz.
    """
    led_pin = "USR3"
    # Configure GPIO pin
    GPIO.setup(led_pin, GPIO.OUT)
    try:
        while True:
            GPIO.output(led_pin, GPIO.HIGH)  # Turn LED on
            time.sleep(1 / (2 * frequency_hz))
            GPIO.output(led_pin, GPIO.LOW)   # Turn LED off
            time.sleep(1 / (2 * frequency_hz))
    except KeyboardInterrupt:
        # Clen up GPIO settings
        GPIO.cleanup()

if __name__ == "__main__":
    blink_frequency = 5  # Frequency in Hz
    blink_usr3_led(blink_frequency)
