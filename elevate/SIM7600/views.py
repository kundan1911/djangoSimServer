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
        calls = ReceivedCall.objects.all()
        
        # Create a list to store processed call data
        processed_calls = []

        # Iterate over each received call
       
        for call in calls:
           
            # Retrieve additional details from CarOwners based on the associated user
            car_owner = call.user

            # Construct a dictionary with combined data from ReceivedCall and CarOwners
            call_data = {
                'id': car_owner.id,
                'phone_number': car_owner.phone_number,
                'timestamp': call.formatted_timestamp,
                'car_number': car_owner.car_number if car_owner else None,
                'parking_slot_number': car_owner.parking_slot_number if car_owner else None
            }
            processed_calls.append(call_data)
        print("innnn")
        # Return the processed call data as JSON
        return JsonResponse({'success': True, 'data': processed_calls})

    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': str(e)})

    

@csrf_exempt
def get_all_recent_log(request):
    try:
        # Retrieve all received calls from the database
        logs = RecentLog.objects.all().order_by('-datetime')
        # Create a list to store processed call data
        recent_data = []

        # Iterate over each received call
        for log in logs:
            log_data = {
                'id':log.ownerId,
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
        type = data.get('type')
        
        # Print the name extracted from the request data
        name = data.get('name', None)
        if name:
            print("Name:", name)

        if type == 1:
            month = data.get('month')
            year = data.get('year')
            # Filter the logs based on the provided month and year
            logs = AllLogs.objects.filter(
                Q(datetime__month=month) & Q(datetime__year=year)
            ).order_by('-datetime')
            
        elif type == 2:
            date = data.get('date')
            # Format the datetime object into the desired string format
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()

            # Filter records based on the selected date
            logs = AllLogs.objects.filter(datetime__date=date_obj).order_by('-datetime')

        else:
            print("else part")
            name = data.get('name')
            # Filter records based on partial or similar name
            logs = AllLogs.objects.filter(name__icontains=name).order_by('-datetime')

        # Serialize the logs data
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
    
@csrf_exempt
def undo_recent_log(request):
    try:
        # Parse request data
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id')
        time = data.get('time')
        
        # Convert time string to datetime object
        # time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        
        
        print(time)
        # Check if there's already an entry in ReceivedCall for the corresponding user
        if not ReceivedCall.objects.filter(user=id).exists():
            # Retrieve the CarOwner object
            
            car_owner = CarOwners.objects.get(id=id)
            print(car_owner)
            # Create a new entry in ReceivedCall
            ReceivedCall.objects.create(user=car_owner)
        else:
            return JsonResponse({'success': False, 'message': 'Call already in the queue'})
 
        # Retrieve RecentLog entry to be undone
        recent_log = RecentLog.objects.get(ownerId=id, datetime=time)
        
        # Delete the RecentLog entry
        recent_log.delete()
        
        return JsonResponse({'success': True, 'message': 'Log undone successfully'})
    except RecentLog.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No matching log found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

@csrf_exempt
def handle_incoming_call(request):
    try:
        data = request.POST.get('phone_number')
        print(data)
        phoneNo = data[3:]
        
        if phoneNo is None:
            return JsonResponse({'success': False, 'error': 'phone number is null'})
        
        # Check whether the caller is a registered user
        try:
            registered_user = CarOwners.objects.get(phone_number=phoneNo)
        except CarOwners.DoesNotExist:
            registered_user = None

        # Initialize callType and callerName
        callType = None
        callerName = None
        print(registered_user.to_dict())
        # Get the channel layer
        channel_layer = get_channel_layer()

        if registered_user is not None:
        # If the caller is a registered user, get their details
            print("new call from registered user")
            callType = 2 if ReceivedCall.objects.filter(user=registered_user).exists() else 1
            callerName = registered_user.name
            
            call_data = {
                'phone_number': registered_user.phone_number,
                'user_id': registered_user.id,
                'car_number': registered_user.car_number,
                'parking_slot_number': registered_user.parking_slot_number,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            # If it's a new call from a registered user, save it in ReceivedCall model
            if callType == 1:
                
                received_call = ReceivedCall(user=registered_user)
                received_call.save()
        else:
            # If the caller is not a registered user, handle accordingly
            callType = 3
            call_data = {
                'phone_number': phoneNo
            }

        # Send the alert message to the WebSocket consumer
        async_to_sync(channel_layer.group_send)(
            "alerts_group",  # Channel group name
            {
                "type": "send_alert",  # Method name to call in consumer
                "message": json.dumps({'type': callType, 'phone_number': call_data})  # Message to send to consumer
            }
        )

        # Return JSON response with success message, call_type, and call_data
        return JsonResponse({'success': True, 'message': 'Call registered successfully', 'call_data': {'call_type': callType, 'name': callerName, 'user_id': call_data.get('user_id')}})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def send_car_ready_sms(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        carOwnerId = data.get('car_owner_id')
        message = 'Your Car is out from the parking'
        # SMSTask.objects.create(phone_number=phone_number, message=message)
        
        carowner = CarOwners.objects.filter(id=carOwnerId).first()
        car_owner = carowner.to_dict()
        phone_number = car_owner.get('phone_number')
        SMSTask.objects.create(phone_number=phone_number, message=message)
        print(carowner)
        call = ReceivedCall.objects.get(user=carowner)
        call.delete()
        # owner = CarOwners.objects.get(phone_number=phone_number)
        # print(owner)
        
        currCarOwnerNo=car_owner.get('car_number') if car_owner else None
        currParkingSlotNo=car_owner.get('parking_slot_number') if car_owner else None
        # Save the call data into RecentLog model
        currCarOwnerName=car_owner.get('name') if car_owner else None
        # Create a new RecentLog instance and save it to the database
        recent_log = RecentLog(ownerId=carOwnerId,name=currCarOwnerName, slot_no=currParkingSlotNo, car_no=currCarOwnerNo)
        recent_log.save()
        print(recent_log)
        all_log = AllLogs(ownerId=carOwnerId,name=currCarOwnerName, slot_no=currParkingSlotNo, car_no=currCarOwnerNo)
        all_log.save()
        print(all_log)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

@csrf_exempt  # Add this decorator to exempt this view from CSRF protection
def off_buzzer(request):
    try:
        message = 'off'
        SMSTask.objects.create(message=message)
        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
@csrf_exempt  # Add this decorator to exempt this view from CSRF protection
def check_server(request):
    try:
        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})