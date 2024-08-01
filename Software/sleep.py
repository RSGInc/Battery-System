import utime
import machine
# Enter deep sleep for a specified duration (in seconds)
# def sleep_with_wakeup(duration_s, switch_pin, switch_start_state, vbus_pin, led):
def sleep_with_wakeup(duration_s, switch_pin, switch_start_state, led):
    sleep_period = 5
    total_sleep_time = duration_s
    led.value(1)
    utime.sleep(0.1)
    led.value(0)
    while total_sleep_time > 0:
        # this is to check if the mode switch has been toggled.
        # Will exit and switch modes if so
        if switch_pin.value() == switch_start_state:
            return
                
        # uncomment if running through thonny
        # utime.sleep(sleep_period)
        # return
    
        # this is to check if it has been plugged into usb
        # because sleeping turns off the usb clock permanently we restart the pico
        # it will then relay data
        # if vbus_pin.value():
            # machine.reset()
        
        sleep_time = min(sleep_period, total_sleep_time)
        total_sleep_time = total_sleep_time - sleep_time
        
        if 0 < sleep_time:
            machine.lightsleep(sleep_time * 1000)
        else:
            utime.sleep(0.1)