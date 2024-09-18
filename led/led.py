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

    if (len(bitmap) != 8 and side in ['l', 'r']) or (len(bitmap) != 16 and side == 'm'):
        print(f'Invalid bitmap length: {len(bitmap)}')
        return
    
    command = f"raw{side}{bitmap}"
    ser.write(command.encode('utf-8'))  # Send the custom bitmap command
    print(f'Sent custom bitmap: {command}')


# Send a preset command
send_preset("happiness")

# Wait and send a custom bitmap for left eyebrow (turn all LEDs on)
time.sleep(3)
send_custom_bitmap('m', 'FFFFFFFFFFFFFFFF')

# Close the serial connection
#ser.close()
