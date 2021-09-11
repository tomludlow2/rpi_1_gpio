import RPi.GPIO as GPIO
import time
import sys
#DHT11 connect to BCM_GPIO14 (Pin 8 on RPi 1)
DHTPIN = 14

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

MAX_UNCHANGE_COUNT = 100

STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5

def read_dht11_dat():
    GPIO.setup(DHTPIN, GPIO.OUT)
    GPIO.output(DHTPIN, GPIO.HIGH)
    time.sleep(0.05)
    GPIO.output(DHTPIN, GPIO.LOW)
    time.sleep(0.02)
    GPIO.setup(DHTPIN, GPIO.IN, GPIO.PUD_UP)

    unchanged_count = 0
    last = -1
    data = []
    while True:
        current = GPIO.input(DHTPIN)
        data.append(current)
        if last != current:
            unchanged_count = 0
            last = current
        else:
            unchanged_count += 1
            if unchanged_count > MAX_UNCHANGE_COUNT:
                break

    state = STATE_INIT_PULL_DOWN

    lengths = []
    current_length = 0

    for current in data:
        current_length += 1

        if state == STATE_INIT_PULL_DOWN:
            if current == GPIO.LOW:
                state = STATE_INIT_PULL_UP
            else:
                continue
        if state == STATE_INIT_PULL_UP:
            if current == GPIO.HIGH:
                state = STATE_DATA_FIRST_PULL_DOWN
            else:
                continue
        if state == STATE_DATA_FIRST_PULL_DOWN:
            if current == GPIO.LOW:
                state = STATE_DATA_PULL_UP
            else:
                continue
        if state == STATE_DATA_PULL_UP:
            if current == GPIO.HIGH:
                current_length = 0
                state = STATE_DATA_PULL_DOWN
            else:
                continue
        if state == STATE_DATA_PULL_DOWN:
            if current == GPIO.LOW:
                lengths.append(current_length)
                state = STATE_DATA_PULL_UP
            else:
                continue
    if len(lengths) != 40:
        return False

    shortest_pull_up = min(lengths)
    longest_pull_up = max(lengths)
    halfway = (longest_pull_up + shortest_pull_up) / 2
    bits = []
    the_bytes = []
    byte = 0

    for length in lengths:
        bit = 0
        if length > halfway:
            bit = 1
        bits.append(bit)
    for i in range(0, len(bits)):
        byte = byte << 1
        if (bits[i]):
            byte = byte | 1
        else:
            byte = byte | 0
        if ((i + 1) % 8 == 0):
            the_bytes.append(byte)
            byte = 0
    checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
    if the_bytes[4] != checksum:
        return False

    return the_bytes[0], the_bytes[2]


def main():
    #Alt Version accepting arguments:

    #Get args:
    #Args stored in sys.argv ['filename', 'arg1' 'arg2']
    mode = 1
    print sys.argv
    if len(sys.argv) > 1 :
        #User has specified values
        num = int(sys.argv[1])
        interval = float(sys.argv[2])
        quiet = sys.argv[3]
        if quiet == "q":
            mode = 0
    else:
        num = 3
        interval = 0.2

    if mode == 1:
        print "Raspberry Pi Temperature and Humidity Program\n"
    i = 0
    temp_reads = []
    humidity_reads = []
    while i < num:
        result = read_dht11_dat()
        if result:
            humidity, temperature = result
            temp_reads.append(temperature)
            humidity_reads.append(humidity)
            if mode == 1:
                print "Reading: Humidity: %s %%,  Temperature: %s C" % (humidity, temperature)
            i =  i+1
            time.sleep(interval)
    
    temp_average = round(sum(temp_reads) / len(temp_reads), 1)
    humidity_average = round(sum(humidity_reads) / len(humidity_reads) ,1)
    if mode == 1:
        print "Success: Completed Data Acquisition"
        print "Temperature Readings: "
        print temp_reads
        print( "Average Temp: ", temp_average, "deg C")

        print "Humuditity Readings: "
        print humidity_reads
        print( "Average Humidity: ", humidity_average, "%");
    else:
        op = str(temp_average) + "," + str(humidity_average)
        print op

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy() 
    finally:
        destroy()

