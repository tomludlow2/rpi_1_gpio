# rpi_1_gpio
GPIO Library for Osoyoo components

Files from the osoyoo kit initially

# Temperature and Humidity
Setup:
- Install the DHT11 module 
- 5V, Gnd, Sensor goes to pin 8 on RPi 1 (GPIO14 if using BRD)

Usage (CLI 1):
- python temp_humdity.py
- Asks how many readings you want to take
- Reads the values back and the average

Usage (Arguments):
- python temp_humidity_arg.py a b c
- Where a is the number of readings you want
- Where b is the number of seconds between readings
-   Note this is a sleep timer, but there the sensor may make this longer than this
- Where c is the mode
-   q = quiet - just outputs a csv of temp,humidity
-   l = loud - outputs a full description
-   j = json - outputs the data in a json string
