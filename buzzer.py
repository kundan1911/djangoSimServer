from pyfirmata import Arduino, util
import time

# Define the Arduino board
board = Arduino('COM26')  # Replace 'COM3' with the port your Arduino is connected to

# Start an iterator thread so serial buffer doesn't overflow
it = util.Iterator(board)
it.start()

# Define the pin for the Buzzer (pin 13 on Arduino Uno)
Buzzer_pin = board.get_pin('d:12:o')  # 'd' stands for digital, 'o' for output

def start_Buzzer():
    Buzzer_pin.write(1)

def stop_Buzzer():
    Buzzer_pin.write(0)

try:
    while True:
        user_input = input("Enter '0' to turn off Buzzer or '1' to turn on Buzzer: ")
        if user_input == '0':
            stop_Buzzer()
        elif user_input == '1':
            start_Buzzer()
        else:
            print("Invalid input! Please enter '0' or '1'.")

except KeyboardInterrupt:
    # Turn off the Buzzer and close the connection when Ctrl+C is pressed
    stop_Buzzer()
    board.exit()
