import utime
import machine
# Enter deep sleep for a specified duration (in seconds)
# this function is confusing
# this is how it waits for a period of time without using much power
# This will be called with duration_s as the duration between readings
# if all works as it should it should divide the duration into chunks of the length sleep period
# and then it should sleep for them and the remainder of the time
def sleep_with_wakeup(duration_s, switch_pin, vbus_pin, led):
    # this sleep period mis how often it should wake to see if it is plugged to a computer or the switch is changed
    sleep_period = 15
    remaining_time = duration_s
    led.value(1)
    utime.sleep(0.1)
    led.value(0)
    while remaining_time > 0:
        # this is to check if the mode switch has been toggled.
        # Will exit and switch modes if so
        if switch_pin.value() == 0:
            return
                
        # uncomment if running through thonny
        # utime.sleep(sleep_period)
        # return
    
        # this is to check if it has been plugged into usb
        # because sleeping turns off the usb clock permanently we restart the pico
        # it will then relay data
        if vbus_pin.value():
            machine.reset()
        
        # it sleeps whatever time is smallest so that it will only sleep one period at a time
        to_sleep = min(sleep_period, remaining_time)
        # subtracts what it is about to sleep
        remaining_time = remaining_time - to_sleep
        
        # sleeps whatever time it just calculated
        if 0 < to_sleep:
            machine.lightsleep(to_sleep * 1000)
        else:
            return