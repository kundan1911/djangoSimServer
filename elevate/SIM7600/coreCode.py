import serial
import time

def send_at_command(ser, command):
    ser.write((command + '\r\n').encode())
    time.sleep(1)
    response = ser.read_all().decode()
    return response

def call_handling(caller_number,ser):
    response = send_at_command(ser, 'AT+CHUP')
    print(f"Hanging up call: {response}")
    if 'OK' in response:
        print("Call hung up.")
        # Wait for a moment before sending SMS (adjust as needed)
        time.sleep(2)
        # Send an SMS to the caller
        send_sms(ser, caller_number, "Thank you for calling. I'll get back to you later.")
    else:
        print(f"Failed to hang up the call. Response: {response}")


def send_sms(ser, phone_number, message):
    #  Send SMS command
    time.sleep(1)
    response = send_at_command(ser, f'AT+CMGS="{phone_number}"')
    print(f"Sending SMS command: {response}")

    # Check for the '>' prompt
    if '>' in response:
        # Send the SMS message
        ser.write((message + chr(26)).encode())
        time.sleep(2)

        # Check for the response
        response = ser.read_all().decode()
        print(f"SMS sending response: {response}")

        if 'OK' or '+CMGS:' in response:
            print("SMS sent successfully.")
        else:
            print(f"Failed to send SMS. Response: {response}")
    else:
        print(f"Failed to send SMS. '>' prompt not received. Response: {response}")


def main():
    # Replace 'COMx' with the correct serial port
    serial_port = 'COM14'

    try:
        ser = serial.Serial(serial_port, baudrate=9600)
        print(f"Connected to {serial_port}")

        # Test communication
        response = send_at_command(ser, 'AT')
        print(f"Testing communication: {response}")

        response = send_at_command(ser, 'AT+CLIP=1')
        print(f"Enabling Caller ID information: {response}")

        # Main loop to continually check for incoming calls
        while True:
            # Check for incoming calls
            #response = send_at_command(ser, 'ATA')
            response = ser.readline().decode().strip()
            print(f"incoming call: {response}")
            if '+CLIP' in response:
                print("Incoming call detected.")
                caller_number = response.split(',')[0].split('"')[1]
                print(f"Extracted phone number: {caller_number}")
                response = send_at_command(ser, 'AT+CHUP')
                print(f"Hanging up call: {response}")
                if 'OK' in response:
                    print("Call hung up.")
                    # Wait for a moment before sending SMS (adjust as needed)
                    time.sleep(1)
                    # Send an SMS to the caller
                    send_sms(ser, caller_number, "Thank you for calling. I'll get back to you later.")
                else:
                    print(f"Failed to hang up the call. Response: {response}")

                    # Sleep for a short interval before checking again (adjust as needed)
                    time.sleep(2)

    except serial.SerialException as e:
        print(f"Error: {e}")

    finally:
        if ser.is_open:
            ser.close()
            print("Serial port closed.")
