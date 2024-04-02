# sim7600/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .coreCode import send_sms, call_handling
import serial
import json
from .models import CarOwners,ReceivedCall,RecentLog,AllLogs,SMSTask
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime
from django.db.models import Q
import time


@csrf_exempt  # Add this decorator to exempt this view from CSRF protection
def make_call(request):
    try:
        serial_port = 'COM14'  # Adjust this according to your setup
        ser = serial.Serial(serial_port, baudrate=9600)
        # Assuming caller_number is passed through request.POST or request.GET
        caller_number = request.POST.get('caller_number')
        call_handling(caller_number, ser)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt  # Add this decorator to exempt this view from CSRF protection
def send_text_message(request):
    try:
        # serial_port = 'COM14'  # Adjust this according to your setup
        # ser = serial.Serial(serial_port, baudrate=9600)
        # Assuming phone_number and message are passed through request.POST or request.GET
        data = json.loads(request.body.decode('utf-8'))
        phone_number = data.get('phone_number')
        message = data.get('message')
        print(data)
        # send_sms(ser, phone_number, message)
        print(phone_number, message)
        # return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt  # Add this decorator to exempt this view from CSRF protection
def new_car_owner(request):
    try:
        
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        name = data.get('name')
        car_number = data.get('car_number')
        phone_number = data.get('phone_number')
        parking_slot_number = data.get('parking_slot_number')

        #check whether any already stored user does not have any value similar to above except name
        if CarOwners.objects.filter(name=name).exists():
            return JsonResponse({'success': False, 'error': 'name already exists'})
        if CarOwners.objects.filter(car_number=car_number).exists():
            return JsonResponse({'success': False, 'error': 'Car number already exists'})
        if CarOwners.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({'success': False, 'error': 'Phone number already exists'})
        if CarOwners.objects.filter(parking_slot_number=parking_slot_number).exists():
            return JsonResponse({'success': False, 'error': 'Parking slot number already exists'})
        
        # Create a new user and save it to the database
        owner = CarOwners(name=name, car_number=car_number, phone_number=phone_number, parking_slot_number=parking_slot_number)
        owner.save()
        # Return a success message in JSON format
        
        return JsonResponse({'success': True, 'message': 'New user created successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

@csrf_exempt  # Add this decorator to exempt this view from CSRF protection
def get_all_car_owners(request):
    try:
        # Retrieve all users from the database
        owners = CarOwners.objects.all()
        # Convert the queryset to a list of dictionaries
        data = [owner.to_dict() for owner in owners]
        # Return the list of users as JSON
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    


@csrf_exempt
def get_all_received_call(request):
    try:
        # Retrieve all received calls from the database
        calls = ReceivedCall.objects.all().order_by('-timestamp')
        
        
        # Create a list to store processed call data
        processed_calls = []

        # Iterate over each received call
        for call in calls:
            # Retrieve additional details from CarOwners based on the phone number
            car_owner = CarOwners.objects.filter(phone_number=call.phone_number).first()

            # Construct a dictionary with combined data from ReceivedCall and CarOwners
            call_data = {
                'phone_number': call.phone_number,
                'timestamp': call.formatted_timestamp,
                'car_number': car_owner.car_number if car_owner else None,
                'parking_slot_number': car_owner.parking_slot_number if car_owner else None
            }
            processed_calls.append(call_data)

        # Return the processed call data as JSON
        return JsonResponse({'success': True, 'data': processed_calls})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

@csrf_exempt
def get_all_recent_log(request):
    try:
        # Retrieve all received calls from the database
        logs = RecentLog.objects.all().order_by('-datetime')
        # Create a list to store processed call data
        # print(calls)
        recent_data = []

        # Iterate over each received call
        for log in logs:
            print("in lp")
            print(f"Name: {log.name}")
            print(f"Slot No: {log.slot_no}")
            print(f"Car Number: {log.car_no}")
            print(f"Formatted Time: {log.formatted_time}")
            # Construct a dictionary with combined data from ReceivedCall and CarOwners
            log_data = {
                'name':log.name,
                'slot_no': log.slot_no,
                'car_number': log.car_no ,
                'time': log.formatted_time  #
            }
            print(log_data)
            recent_data.append(log_data)
        print(recent_data)
        # Return the processed call data as JSON
        return JsonResponse({'success': True, 'data': recent_data})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def get_all_log(request):
    try:
        # Retrieve all received calls from the database
        logs = AllLogs.objects.all().order_by('-datetime')
        # Create a list to store processed call data
        # print(calls)
        logs_data = []

        # Iterate over each received call
        for log in logs:
            print("in lp")
            # print(f"Name: {log.name}")
            # print(f"Slot No: {log.slot_no}")
            # print(f"Car Number: {log.car_no}")
            # print(f"Formatted Time: {log.formatted_date}")
            # Construct a dictionary with combined data from ReceivedCall and CarOwners
            log_data = {
                'name':log.name,
                'slot_no': log.slot_no,
                'car_number': log.car_no ,
                'time': log.formatted_time,  #
                'date':log.formatted_date
            }
            # print(log_data)
            logs_data.append(log_data)
        print(logs_data)
        # Return the processed call data as JSON
        return JsonResponse({'success': True, 'data': logs_data})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
@csrf_exempt  # Add this decorator to exempt this view from CSRF protection
def get_car_owner_detail(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        car_number = data.get('car_number')
        print(car_number)
        phone_number = data.get('phone_number')
        if(phone_number is None):
            owner = CarOwners.objects.get(car_number=car_number)
            # above is not a json object , change it to json object
            owner = json.dumps(owner.to_dict())
            print(owner)
            return JsonResponse({'success': True, 'data': owner})
        else:
            owner = CarOwners.objects.get(phone_number=phone_number)
            print(owner)
            return JsonResponse({'success': True, 'data': owner})
        
        # Retrieve the user with the given car number from the database    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
@csrf_exempt
def get_particular_logs(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        
        # Extract month and year from the request data
        type=data.get('type')
        
        
        if type==1:
            month = data.get('month')
            year = data.get('year')
        # Filter the logs based on the provided month and year
            logs = AllLogs.objects.filter(
                Q(datetime__month=month) & Q(datetime__year=year)
            ).order_by('-datetime')
            
            # Serialize the logs data
            serialized_logs = [{
                'name': log.name,
                'slot_no': log.slot_no,
                'car_number': log.car_no,
                'date': log.formatted_date,
                'time': log.formatted_time
            } for log in logs]
            
            return JsonResponse({'success': True, 'logs': serialized_logs})
        elif type==2:
            date = data.get('date')

# Format the datetime object into the desired string format
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()

            # Filter records based on the selected date
            logs_for_selected_date = AllLogs.objects.filter(datetime__date=date_obj).order_by('-datetime')
             # Serialize the logs data
            serialized_logs = [{
                'name': log.name,
                'slot_no': log.slot_no,
                'car_number': log.car_no,
                'date': log.formatted_date,
                'time': log.formatted_time
            } for log in logs_for_selected_date]
            return JsonResponse({'success': True, 'logs': serialized_logs})

        else:
            print("else partt")
            name=data.get('name')
            # convert name into lowercase
            name=name.lower()
            print(name)
            logs = AllLogs.objects.filter(name=name).order_by('-datetime')
            
            serialized_logs = [{
                'name': log.name,
                'slot_no': log.slot_no,
                'car_number': log.car_no,
                'date': log.formatted_date,
                'time': log.formatted_time
            } for log in logs]
            return JsonResponse({'success': True, 'logs': serialized_logs})


    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt  # Add this decorator to exempt this view from CSRF protection
def update_owner_data(request):
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    carNoToUpdate=data.get('OwnerToUpdate');
    newOwnerData=data.get('newOwnerData');
    print(newOwnerData)
    try:
        owner = CarOwners.objects.get(car_number=carNoToUpdate)
        owner.name = newOwnerData.get('name')
        owner.car_number = newOwnerData.get('car_number')
        owner.phone_number = newOwnerData.get('phone_number')
        owner.parking_slot_number = newOwnerData.get('parking_slot_number')
        owner.save()
        return JsonResponse({'success': True, 'message': 'Car owner updated successfully'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    


@csrf_exempt  # Add this decorator to exempt this view from CSRF protection
def delete_owner_data(request):
    # need to delete owner data on the basis of car number
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    carNoToDelete = data.get('OwnerToDeleteCarNo')
    try:
        owner = CarOwners.objects.get(car_number=carNoToDelete)
        owner.delete()
        return JsonResponse({'success': True, 'message': 'Car owner deleted successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
@csrf_exempt  # Add this decorator to exempt this view from CSRF protection
def undo_recent_log(request):
    # Parse request data
    data = json.loads(request.body.decode('utf-8'))
    log_name = data.get('name')
    slot_no = data.get('slot_no')
    print(data)
    try:
        # Query RecentLog based on name and formatted_time
        recent_logs = RecentLog.objects.filter(name=log_name, slot_no=slot_no)
        
        if recent_logs.exists():
            # Delete the first matching entry
            recent_logs.first().delete()
            owner = CarOwners.objects.get(name=log_name)
            car_owner = owner.to_dict()
            print(car_owner)
            receiveCall = ReceivedCall(phone_number=car_owner.get('phone_number'))
            receiveCall.save()
            return JsonResponse({'success': True, 'message': 'Log undone successfully'})
        else:
            return JsonResponse({'success': False, 'error': 'No matching log found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
@csrf_exempt  # Add this decorator to exempt this view from CSRF protection
def handle_incoming_call(request):
    try:
        # Send WebSocket message to frontend
       # Get the channel layer
        # data = json.loads(request.body.decode('utf-8'))
        data = request.POST.get('phone_number')
        print(data)
        phoneNo=data[3:]
        # mssg=data.get('message')
        if(phoneNo is None):
            return JsonResponse({'success': False, 'error': 'phone number is null'})
        
        #check whether any already stored user does not have same phone NO
        alreadyCallRegister=False
        if ReceivedCall.objects.filter(phone_number=phoneNo).exists():
            alreadyCallRegister=True

        channel_layer = get_channel_layer()
        if(alreadyCallRegister):
            owner = CarOwners.objects.get(phone_number=phoneNo)
            car_owner = owner.to_dict()  # Assuming this method returns a dictionary
        
            print(car_owner)
            call_data = {
                'phone_number': phoneNo,
                # 'timestamp': car_owner.timestamp.strftime('%Y-%m-%d %H:%M:%S'),  # Format timestamp as string
                'car_number': car_owner.get('car_number') if car_owner else None,
                'parking_slot_number': car_owner.get('parking_slot_number')  if car_owner else None
            }
            async_to_sync(channel_layer.group_send)(
            "alerts_group",  # Channel group name
            {
                "type": "send_alert",  # Method name to call in consumer
                "message": json.dumps({'type':"SameOwnerCall",'phone_number':call_data})  # Message to send to consumer
            }
            )
            currCarOwnerNo=car_owner.get('car_number') if car_owner else None
            currParkingSlotNo=car_owner.get('parking_slot_number') if car_owner else None
            currCarOwnerName=car_owner.get('name') if car_owner else None
            # Create a new RecentLog instance and save it to the database
            recent_log = RecentLog(name=currCarOwnerName,slot_no=currParkingSlotNo,car_no=currCarOwnerNo)
            recent_log.save()
            all_log = AllLogs(name=currCarOwnerName,slot_no=currParkingSlotNo,car_no=currCarOwnerNo)
            all_log.save()
        else:
            receiveCall = ReceivedCall(phone_number=phoneNo)
            receiveCall.save()
            car_owner = CarOwners.objects.filter(phone_number=phoneNo).first()
            currCarOwnerNo=car_owner.get('car_number') if car_owner else None
            currParkingSlotNo=car_owner.get('parking_slot_number') if car_owner else None
            call_data = {
                'phone_number': phoneNo,
                # 'timestamp': car_owner.timestamp.strftime('%Y-%m-%d %H:%M:%S'),  # Format timestamp as string
               'car_number': currCarOwnerNo,
                'parking_slot_number': currParkingSlotNo
            }
             # Send the alert message to the WebSocket consumer
            async_to_sync(channel_layer.group_send)(
            "alerts_group",  # Channel group name
            {
                "type": "send_alert",  # Method name to call in consumer
                "message": json.dumps({'type':"NewOwnerCall",'phone_number':call_data})  # Message to send to consumer
            }
            )
            # Save the call data into RecentLog model
            currCarOwnerName=car_owner.get('name') if car_owner else None
            # Create a new RecentLog instance and save it to the database
            recent_log = RecentLog(currCarOwnerName,currParkingSlotNo,currCarOwnerNo)
            recent_log.save()

            all_log=AllLogs(currCarOwnerName, currParkingSlotNo, currCarOwnerNo)
            all_log.save()


        
        return JsonResponse({'success': True, 'message': 'Call registered successfully'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

@csrf_exempt
def send_car_ready_sms(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        phone_number = data.get('phone_number')
        message = 'Your Car is out from the parking'
        SMSTask.objects.create(phone_number=phone_number, message=message)
        call = ReceivedCall.objects.get(phone_number=phone_number)
        call.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})