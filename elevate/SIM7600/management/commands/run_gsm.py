import threading
import time
import serial
import json
import requests
from django.core.management.base import BaseCommand
from SIM7600.coreCode import send_sms, send_at_command
from SIM7600.models import SMSTask
# from SIM7600.management.commands.buzzer import start_Buzzer, stop_Buzzer

# buzzer_control.py

from pyfirmata import Arduino, util
import time


class Command(BaseCommand):
    help = 'Run GSM service to monitor for incoming calls and handle SMS'
    board = Arduino('COM26')  # Replace 'COM3' with the port your Arduino is connected to

    # Start an iterator thread so serial buffer doesn't overflow
    it = util.Iterator(board)
    it.start()

    # Define the pin for the Buzzer (pin 13 on Arduino Uno)
    global Buzzer_pin
    Buzzer_pin = board.get_pin('d:12:o')  # 'd' stands for digital, 'o' for output

    def start_Buzzer():
        # Buzzer_pin.write(1)
        print("Buzzer ON")

    def stop_Buzzer():
        Buzzer_pin.write(0)
        print("Buzzer OFF")

    def handle(self, *args, **options):
        # Replace 'COMx' with the correct serial port
        serial_port = 'COM19'
        ser = None

        while True:
            try:
                if ser is None or not ser.is_open:
                    ser = serial.Serial(serial_port, baudrate=9600)
                    self.stdout.write(self.style.SUCCESS(f"Connected to {serial_port}"))

                    # Send initialization commands
                    response = send_at_command(ser, 'AT')
                    self.stdout.write(self.style.SUCCESS(f"Testing communication: {response}"))

                    response = send_at_command(ser, 'AT+CLIP=1')
                    self.stdout.write(self.style.SUCCESS(f"Enabling Caller ID information: {response}"))

                # Start threads for monitoring calls and processing SMS tasks
                call_thread = threading.Thread(target=self.monitor_calls, args=(ser,))
                sms_thread = threading.Thread(target=self.process_sms_tasks, args=(ser,))

                call_thread.start()
                sms_thread.start()

                # Wait for threads to finish (which they won't, hence the use of while True loops)
                call_thread.join()
                sms_thread.join()

            except serial.SerialException as e:
                self.stdout.write(self.style.ERROR(f"Error: {e}"))
                time.sleep(1)  # Wait for a while before attempting reconnection

    def monitor_calls(self, ser):
        while True:
            try:
                response = ser.readline().decode().strip()
                self.stdout.write(self.style.SUCCESS(f"Incoming call: {response}"))
                if '+CPIN: READY' in response:
                    if ser.is_open:
                        ser.close()
                        print("Serial port closed.")
                        time.sleep(1)
                        Command.handle(self)
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
                        response_data = response.json()
                        call_data = response_data.get('call_data', {})  # Use get() with a default value to handle missing key
                        call_type = call_data.get('call_type')  # Use get() with a default value to handle missing key
                        name = call_data.get('name')  # Use get() with a default value to handle missing key
                        if call_type == 1:
                            Command.start_Buzzer()
                            send_sms(ser, caller_number, "Hey {}, Your call has been registered. We will notify when your car is ready.".format(name))
                        elif call_type == 2:
                            send_sms(ser, caller_number, "Hey {}, Your call was already registered. You will be notified when the car is ready".format(name))
                        else:
                            send_sms(ser, caller_number, "You are not a registered user. Please contact the valet")
                        time.sleep(1)
                        
                    else:
                        self.stdout.write(self.style.ERROR(f"Failed to hang up the call. Response: {response}"))
                        time.sleep(2)
                time.sleep(0.5)
            except serial.SerialException:
                pass  # Handle serial communication errors

    def process_sms_tasks(self, ser):
        while True:
            try:
                pending_tasks_count = SMSTask.objects.count()
                if pending_tasks_count > 0:
                    task = SMSTask.objects.first()  # Get the first pending task
                    if(task.message=="off"):
                        Command.stop_Buzzer()
                    else:
                        send_sms(ser, task.phone_number, task.message)
                    task.delete()
            except serial.SerialException:
                pass  # Handle serial communication errors