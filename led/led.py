import serial #pip install pyserial
import time

# Initialize the serial connection
ser = serial.Serial(
    port='COM4',       # Port connected to the Arduino
    baudrate=9600,     # Baudrate for the communication
    bytesize=serial.EIGHTBITS,  # 8 data bits
    parity=serial.PARITY_NONE,  # No parity bit
    stopbits=serial.STOPBITS_ONE,  # 1 stop bit
    timeout=1          # Read timeout, adjust as needed
)
time.sleep(1)  # Give some time to establish the connection

# Function to send preset command
def send_preset(preset):
    valid_presets = (
        "happiness",
        "sadness",
        "anger",
        "disgust",
        "surprise",
        "fear",
        "neutral",
        "clear"
    )
    
    if preset in valid_presets:
        ser.write(preset.encode('utf-8'))  # Send the preset command
        print(f'Sent preset: {preset}')
    else:
        print(f'Invalid preset: {preset}')

# Function to send custom bitmap command
def send_custom_bitmap(side, bitmap):
    if side not in ['l', 'r', 'm']:
        print(f'Invalid side: {side}')
        return

    if (len(bitmap) != 16 and side in ['l', 'r']) or (len(bitmap) != 32 and side == 'm'):
        print(f'Invalid bitmap length: {len(bitmap)}')
        return
    
    command = f"raw{side}{bitmap}"
    ser.write(command.encode('utf-8'))  # Send the custom bitmap command
    print(f'Sent custom bitmap: {command}')

presets = (
    "happiness",
    "sadness",
    "anger",
    "disgust",
    "surprise",
    "fear",
    "neutral",
    "clear"
)
for preset in presets:
    print("press enter ...")
    input()
    send_preset(preset)

print('done')

# Send a preset command
send_preset("happiness")

# Wait and send a custom bitmap for left eyebrow (turn all LEDs on)
time.sleep(3)

send_custom_bitmap('m', 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
# 64mm x 32mm, hole 3m 8x16
"""
21 41 ...
22 42
23 43
24 44
11 31
12 32
13 33
14 34
"""

send_custom_bitmap('l', 'FFFFFFFFFFFFFFFF')
"""
... 31 11
    32 12
    33 13
    34 14
    41 21
    42 22
    43 23
    44 24
"""

#send_custom_bitmap('m', 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF') # full mouth

send_custom_bitmap('m', '00000078848484848484848484780000') # == send_preset('anger')
time.sleep(2)
send_custom_bitmap('m', '00000078848444484848448484780000') # better anger
time.sleep(2)

#send_preset('disgust')
#send_custom_bitmap('m', '000080C040202028282828485020C000')

# Close the serial connection
ser.close()
