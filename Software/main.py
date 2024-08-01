import machine
import utime
from ht16k33 import HT16K33MatrixFeatherWing
from read import read_channels_setup, read_channels_log
from file import relay_data
from sleep import sleep_with_wakeup

# Define the onboard LED pin 
status_led = machine.Pin(3, machine.Pin.OUT)

# get rid of this later
while True:
    status_led.value(1)  
    utime.sleep_ms(100)
    status_led.value(0)
    utime.sleep_ms(100)

# Define GPIO pin used for the switch input
SWITCH_PIN = 2

# Global variable to control the number of batteries the mux looks for.
# 31
num_batteries = 27

# Define the sleep period in seconds
sleep_period = 10

# Define a class to hold the voltage and connection status of each battery
class Battery:
    def __init__(self):
        self.voltage = 0.0
        self.current = 0.0
        self.level = 0.0
        self.offset = 0.0 # voltage when real voltage is 0
        self.gain = 0.0 # actual = gain x reading - offset
        

# Initialize switch input pin
switch_pin = machine.Pin(SWITCH_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)

# for pico W
# vbus_pin = machine.Pin('WL_GPIO2', machine.Pin.IN)
# For normal pico and other board
# vbus_pin = machine.Pin(24, machine.Pin.IN, machine.Pin.PULL_DOWN)



# initalize i2c connection to led driver
i2c = machine.I2C(0, scl=machine.Pin(13), sda=machine.Pin(12))
utime.sleep_ms(100)
    
display = HT16K33MatrixFeatherWing(i2c)










# Main function
# Main function
def main():
    
    
    logging = 0
    
    switch_start_state = switch_pin.value()
    
    
    # all made from use with the calibration folder Q:\Administrative\Acoustics Admin & Resources\Resources\Equipment & Supporting Software\Battery System\Python\Calibration
    offsets = [.157, 0.157778182, 0.157664634, 0.156089091, 0.155693333, 0.15524, 0.154372727, 0.154155152, 0.153857576, 0.157060606, 0.156813939, 0.156264458, 0.156164458, 0.154946667, 0.154364848, 0.157550602, 0.183667879, 0.181670909, 0.18039697, 0.179233939, 0.177347273, 0.180369277, 0.181682424, 0.180920606, 0.180455758, 0.178446667, 0.177653939]
    # measure when given 5.29v
    actual = 3.5
    measured = [3.3881, 3.37176, 3.362066667, 3.38526, 3.35526, 3.36192, 3.38458, 3.37774, 3.3599, 3.37352, 3.37628, 3.3587, 3.3816, 3.36592, 3.3705, 3.36845, 3.37758, 3.38748, 3.37986, 3.37052, 3.37982, 3.382525, 3.37996, 3.37818, 3.38714, 3.37514, 3.38326]
    
    # Array to hold the status of each battery
    batteries = [Battery() for _ in range(num_batteries)]
    
    # calculates and updates gains and offsets
    for i in range(len(batteries)):
        batteries[i].offset = offsets[i]
        batteries[i].gain = (actual + offsets[i]) / measured[i]
        
    # this section needs to be commented to run on thonny
    # check if usb is connected and run relay data if so
    # if vbus_pin.value():
        #display.power_off()
        #status_led.value(1)  
        # relay_data(vbus_pin, status_led)
        #status_led.value(0)
    #else:
        #status_led.value(0)  

    while True:
        display.power_on()
        # SETUP
        while switch_pin.value() == switch_start_state:
            read_channels_setup(batteries, display, num_batteries)
            # if it gets plugged into usb it resets
            # when it resets it will begin relaying data
            # needs to be commented to run on thonny
            # if vbus_pin.value():
                # machine.reset()

            
        # LOGGING
        while not switch_pin.value() == switch_start_state:
            display.power_off()


            # Read battery voltages and log data
            logging = read_channels_log(batteries, num_batteries, logging)
                
            # function for extended periods of sleeping
            # sleep_with_wakeup(10, switch_pin, switch_start_state, vbus_pin, status_led)
            sleep_with_wakeup(15, switch_pin, switch_start_state, status_led) 
# Run the main function
# not sure if this is actually needed
if __name__ == "__main__":
    main()









