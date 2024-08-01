import machine

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