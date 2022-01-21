#Libraries
import RPi.GPIO as GPIO
import time
import sys
import mido

 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
 
 
def distance(trigger_pin, echo_pin):
    #set GPIO direction (IN / OUT)
    GPIO.setup(trigger_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)
    # set Trigger to HIGH
    GPIO.output(trigger_pin, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trigger_pin, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echo_pin) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(echo_pin) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def send_cc(control_code, value):
    msg = mido.Message("control_change", channel=0, control=control_code, value=int(value))
    print(msg)
    outport.send(msg)
 
if __name__ == '__main__':

    for port in mido.get_output_names():
        if port[:9]=="UNO Synth":
            outport = mido.open_output(port)
            print("Using Output:", port)
            break


    if outport == None:
        sys.exit("Unable to find UNO Synth")

    try:
        while True:
            dist_1 = int(distance(17, 24)-2)
            dist_2 = int(distance(18, 23)-2)
            print(f'Measured Distances {dist_1} cm and {dist_2} cm.')

            if dist_1 < 50:
                send_cc(17, 127/50*dist_1)

            if dist_2 < 50:
                send_cc(20, 127/50*dist_2)

            time.sleep(0.1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

