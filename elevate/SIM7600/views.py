# sim7600/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .coreCode import send_sms, call_handling
import serial
import json
from .models import CarOwners
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
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
        websocketTestingview(request)
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
def websocketTestingview(request):
    try:
        # Send WebSocket message to frontend
       # Get the channel layer
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        phoneNo=data.get('phone_number')
        mssg=data.get('message')
        channel_layer = get_channel_layer()
        # print(channel_layer)
        # Send the alert message to the WebSocket consumer
        async_to_sync(channel_layer.group_send)(
            "alerts_group",  # Channel group name
            {
                "type": "send_alert",  # Method name to call in consumer
                "message": json.dumps({'type':"NewOwnerCall",'phone_number':"caller_number"})  # Message to send to consumer
            }
        )

        return JsonResponse({'success': True, 'message': 'Websocket testing successful'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})