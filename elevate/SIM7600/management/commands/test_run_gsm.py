import threading
import time
import serial
import json
import requests
from django.core.management.base import BaseCommand
from SIM7600.coreCode import send_sms, send_at_command
from SIM7600.models import SMSTask


class Command(BaseCommand):
    help = 'Run GSM service to monitor for incoming calls and handle SMS'

    def handle(self, *args, **options):
        # Replace 'COMx' with the correct serial port
        serial_port = 'COM19'

        try:
            ser = serial.Serial(serial_port, baudrate=9600)
            self.stdout.write(self.style.SUCCESS(f"Connected to {serial_port}"))

            # Test communication
            response = send_at_command(ser, 'AT')
            self.stdout.write(self.style.SUCCESS(f"Testing communication: {response}"))

            response = send_at_command(ser, 'AT+CLIP=1')
            self.stdout.write(self.style.SUCCESS(f"Enabling Caller ID information: {response}"))

            # Define function to monitor incoming calls
            def monitor_calls():
                while True:
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
                            data = {'type': "NewOwnerCall", 'phone_number': caller_number}
                            url = 'http://localhost:8000/handle_incoming_call'
                            response = requests.post(url, data=data)
                            print(response.json())
                            time.sleep(1)
                            send_sms(ser, caller_number, "Thank you for calling. I'll get back to you later.")
                        else:
                            self.stdout.write(self.style.ERROR(f"Failed to hang up the call. Response: {response}"))
                            time.sleep(2)

            # Define function to process pending SMS tasks
            # Function to check for pending SMS tasks
            def process_sms_tasks():
                while True:
                    pending_tasks_count = SMSTask.objects.count()
                    if pending_tasks_count == 1:
                        task = SMSTask.objects.first()  # Get the first pending task
                        send_sms(ser, task.phone_number, task.message)
                        task.delete()
                    # time.sleep(60)  # Check for pending tasks every 60 seconds

            # Start threads for monitoring calls and processing SMS tasks
            call_thread = threading.Thread(target=monitor_calls)
            sms_thread = threading.Thread(target=process_sms_tasks)

            call_thread.start()
            sms_thread.start()

            # Wait for threads to finish (which they won't, hence the use of `while True` loops)
            while True:
                time.sleep(1)

        except serial.SerialException as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))

        finally:
            if ser.is_open:
                ser.close()
                self.stdout.write(self.style.SUCCESS("Serial port closed."))

