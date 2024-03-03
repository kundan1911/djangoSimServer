# sim7600/management/commands/run_gsm.py

import serial
import time
import json
from django.core.management.base import BaseCommand
import requests
from SIM7600.coreCode import send_at_command, call_handling, send_sms


class Command(BaseCommand):
    help = 'Run GSM service to monitor for incoming calls and handle SMS'

    def handle(self, *args, **options):
        # Replace 'COMx' with the correct serial port
        serial_port = 'COM14'

        try:
            ser = serial.Serial(serial_port, baudrate=9600)
            self.stdout.write(self.style.SUCCESS(f"Connected to {serial_port}"))

            # Test communication
            response = send_at_command(ser, 'AT')
            self.stdout.write(self.style.SUCCESS(f"Testing communication: {response}"))

            response = send_at_command(ser, 'AT+CLIP=1')
            self.stdout.write(self.style.SUCCESS(f"Enabling Caller ID information: {response}"))

            # Main loop to continually check for incoming calls
            while True:
                # Check for incoming calls
                response = ser.readline().decode().strip()
                self.stdout.write(self.style.SUCCESS(f"Incoming call: {response}"))
                if '+CLIP' in response:
                    self.stdout.write(self.style.SUCCESS("Incoming call detected."))
                    caller_number = response.split(',')[0].split('"')[1]
                    self.stdout.write(self.style.SUCCESS(f"Extracted phone number: {caller_number}"))
                    response = send_at_command(ser, 'AT+CHUP')
                    self.stdout.write(self.style.SUCCESS(f"Hanging up call: {response}"))
                    if 'OK' in response:
                        self.stdout.write(self.style.SUCCESS("Call hung up."))
                        # Wait for a moment before sending SMS (adjust as needed)
                        data = {'type':"NewOwnerCall",'phone_number':caller_number}  # Example data to send
                        url = 'http://localhost:8000/handle_incoming_call/'  # URL of the Django server's view
                        response = requests.post(url, data=data)
                        print(response.json())
                        time.sleep(1)
                        # Send an SMS to the caller
                        send_sms(ser, caller_number, "Thank you for calling. I'll get back to you later.")
                    else:
                        self.stdout.write(self.style.ERROR(f"Failed to hang up the call. Response: {response}"))

                        # Sleep for a short interval before checking again (adjust as needed)
                        time.sleep(2)

        except serial.SerialException as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))

        finally:
            if ser.is_open:
                ser.close()
                self.stdout.write(self.style.SUCCESS("Serial port closed."))
