# sms_utils.py

import serial
from SIM7600.coreCode import send_sms

def send_sms_to_caller(caller_number, message):
    try:
        serial_port = 'COM19'  # Adjust this according to your setup
        ser = serial.Serial(serial_port, baudrate=9600)
        send_sms(ser, caller_number, message)
        ser.close()
        return True
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False