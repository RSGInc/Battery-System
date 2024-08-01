import machine
import utime
# Function to read battery data during logging
# it first reads all of the data from batteries by calling other functions
# it then checks to see if it is connected to 12v
# it then calculates what the total power consumption is
# theres two ways it does this
#
# 
def read_channels_log(batteries, num_batteries, logging):
    # total current and audio current are the currents used to calculate the total wattage for 4v, 12v and audio
    total_current = 0
    audio_current = 0
    
    # this tells it if it is supplying 12v
    # during this it also reads the battery voltage and currents in
    twelve_volt = False
    for channel in range(num_batteries):
        # reading battery v and a
        if batteries[channel].level or channel < 1:  # Always read 4V voltage
            # Read voltage from the current channel
            read_channel(batteries, channel)
        # see if it is power 12v
        if batteries[channel].level == 12:
            twelveVolt = True
            

    if twelveVolt:
        
        four_v = 0
        eight_v = 0
        twelve_v = 0
        for channel in range(num_batteries):
            # 4v sum
            if channel >= 3 and channel <= 8:
                four_v += batteries[channel].current
            # 8v sum
            if channel >= 9 and channel <= 14:
                eight_v += batteries[channel].current
            # 12v sum
            if channel >= 15 and channel <= 20:
                twelve_v += batteries[channel].current
            # audio sum
            if channel >= 21:
                audio_current += batteries[channel].current
        # averages the currents, stores the data to local file and returns from the function
        # This would be for the cirrus
        if audio_current:
            total_current = (four_v + eight_v + twelve_v) / 2
            for channel in range(num_batteries):
                if channel > 20 and batteries[channel].level:
                    audio_current += batteries[channel].current
        else:
            total_current = (four_v + eight_v + twelve_v) / 3
        return store_to_local_file(batteries, total_current, audio_current, num_batteries, logging)
    
    # this is for when only using 12v it just sums the total current
    else:      
        for channel in range(num_batteries):
            if channel < 21:
                total_current += batteries[channel].current
            if channel > 20:
                audio_current += batteries[channel].current
        return store_to_local_file(batteries, total_current, audio_current, num_batteries, logging)



# Function to populate batteries during setup
def read_channels_setup(batteries, display, num_batteries):
    for channel in range(num_batteries):
        read_channel(batteries, channel)
        if batteries[channel].voltage > 9:
            batteries[channel].level = 12
        elif batteries[channel].voltage > 5:
            batteries[channel].level = 8
        elif batteries[channel].voltage > 1:
            batteries[channel].level = 4
        else:
            batteries[channel].level = 0
    # Update LEDs
    update_leds(batteries, display, num_batteries)




mux1_pins = [machine.Pin(i, machine.Pin.OUT) for i in [17, 16, 15, 14]]
mux2_pins = [machine.Pin(i, machine.Pin.OUT) for i in [21, 20, 19, 18]]

# Function to set the control pins of the multiplexer
def set_mux_channel(channel):
    # have to do this weird thing with the mux channels because I wired these up in a kinda stupid way
    #hopefully this will be fixed and switched to something normal
    if channel < 16:
        for i in range(4):
            mux1_pins[i].value((channel >> i) & 0x01)
            mux2_pins[i].value(0)
    else:
        for i in range(4):
            mux2_pins[i].value((channel - 15 >> i) & 0x01)
    utime.sleep_ms(1)



# Function to read voltage from a specific MUX channel
def read_average_voltage_from_mux_channel(channel):
    
    # Initialize ADC
    adc = machine.ADC(machine.Pin(26))

    
    num_samples = 40

    # Set MUX to the specified channel
    set_mux_channel(channel)

    # Collect all voltage readings
    voltage_readings = []
    for _ in range(num_samples):
        # Read raw ADC value
        result = adc.read_u16()

        # Convert the raw ADC value to voltage (assuming a 3.3V reference)
        voltage = 5.7 * result * 3.3 / 65535  # 16-bit ADC, so 2^16 = 65535, voltage divider with 10k and 47k

        # Accumulate the voltage readings
        voltage_readings.append(voltage)

    # Calculate the initial average voltage
    initial_average = sum(voltage_readings) / num_samples

    # Filter out readings that are greater than 10% off the initial average
    filtered_readings = [v for v in voltage_readings if abs(v - initial_average) <= 0.1 * initial_average]

    # Calculate the new average from the filtered readings
    if filtered_readings:
        average_voltage = sum(filtered_readings) / len(filtered_readings)
    else:
        # If all readings are filtered out (which is unlikely but possible in edge cases),
        # the function returns the initial average to avoid division by zero.
        average_voltage = initial_average

    return average_voltage





# Function to control LEDs based on battery connection status
def update_leds(batteries, display, num_batteries):
    for i in range(0, num_batteries - 3):
        if batteries[i + 3].level:
            display.plot(i // 6, i % 6).draw()
        else:
            display.plot(i // 6, i % 6, 0).draw()
        

        
        

def store_to_local_file(batteries, total_current, audio_current, num_batteries, logging):
    # this sees what voltage the slm is being powered at (4v, 8v, 12v)
    current_level = 0
    for i in range(3, 20):
        if batteries[i].level > current_level:
            current_level = batteries[i].level
            
    # Clear the contents of the file only if logging has not started yet
    if not logging:
        with open("battery_data.csv", "w") as file:
            file.write("Power Consumption (W)")
            if audio_current > 1:
                file.write(", Audio Power (W)")
            file.write(", 4v Supply (V)")
            if batteries[2].level:
                file.write(", 12v Supply (V)")
            for i in range(3, num_batteries):
                if batteries[i].level:
                    file.write(f", Battery {i - 2} Voltage (V)")
                    file.write(f", Battery {i - 2} Current (A)")
            
            file.write("\n")
        logging = True
        
    with open("battery_data.csv", "a") as file:
        if current_level == 12:
            power = batteries[2].voltage * total_current
            file.write(f"{power:.4f}")
        else:
            power = batteries[0].voltage * total_current
            file.write(f"{power:.4f}")
        if audio_current > .1:
            power = batteries[0].voltage * audio_current
            file.write(f"{power:.4f}")
        file.write(f", {batteries[0].voltage:.4f}")
        for i in range(2, num_batteries):
            if batteries[i].level and (i == 2):
                file.write(f", {batteries[i].voltage:.4f}")
            elif batteries[i].level:
                file.write(f", {batteries[i].voltage:.4f}")
                file.write(f", {batteries[i].current:.4f}")
        file.write("\n")
    return logging
    
    
    
    
def read_channel(batteries, channel):
    voltage = read_average_voltage_from_mux_channel(channel)
    # Update battery voltage
    batteries[channel].voltage = (voltage * batteries[channel].gain) - batteries[channel].offset
    # update battery current
    if batteries[channel].level == 12:
        batteries[channel].current = (batteries[channel].voltage - batteries[2].voltage) / 10.3
    elif batteries[channel].level == 8:
        batteries[channel].current = (batteries[channel].voltage - batteries[1].voltage) / 10.3
    elif batteries[channel].level == 4:
        batteries[channel].current = (batteries[channel].voltage - batteries[0].voltage) / 10.3




