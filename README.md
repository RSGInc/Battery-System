# Battery-System
#### A brand new board will need firmware and software loaded onto it
## We will need python installed to operate this
####  While using the installer, make sure you check the box “Add Python to PATH.” Next, click “Customize installation” and check the “pip” box under Optional Features. Then, click “Next” to get to Advanced Options and check the “Add Python to environment variables” box.
https://www.python.org/downloads/
## To use mpremote, install it first using pip
`py -m pip install --user mpremote`

## To load the firmware into the device
1. To start, open the Firmware folder and download the .uf2 file.
2. Plug in the battery board while pressing the white button
3. You should see a drive called RPI-RP2 appear in your file explorer
4. Drag and drop the firmware file to this drive

## To load the software onto the device 
5. Open a command line and paste `py -m mpremote mip install github:RSGInc/Battery-System/Software`
   The code will not run until the device is unplugged





## To clear the devices memory completely
#### Only do this if the device is hung and will not respond to thonny or any inputs
1. Open the Clear-Flash folder and download the .uf2 file.
2. Plug in the battery board while pressing the white button
3. You should see a drive called RPI-RP2 appear in your file explorer
4. Drag and drop the firmware file to this drive
5. Firmware and software will need to be reuploaded to the board

