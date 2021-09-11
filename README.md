# rpi_1_gpio
GPIO Library for Osoyoo components

Files from the osoyoo kit initially

# Temperature and Humidity
Setup:
- Install the DHT11 module 
- 5V, Gnd, Sensor goes to pin 8 on RPi 1 (GPIO14 if using BRD)

Usage (CLI 1):
> python temp_humdity.py
> Asks how many readings you want to take
> Reads the values back and the average