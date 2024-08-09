import machine

# to be used with "Q:\Administrative\Acoustics Admin & Resources\Resources\Equipment & Supporting Software\Battery System\Connect_to_Pico\_info\connect_to_pico.py"
# that would be run on your computer
# This just prints "Transfering Data." then everything in the csv file, then "Transfer Completed.\n"
def relay_data(vbus_pin, led):
    while True:
        with open("battery_data.csv", mode='r') as file:
            print("Transfering Data.")
            # Read the first line as headers
            for line in file:
                strippedLine = line.strip()
                print(strippedLine)

            # Print transfer completion message
            print("Transfer Completed.\n")
        if not vbus_pin.value():
            led.value(0)  # Turn the LED off if GPIO 24 is high
            break