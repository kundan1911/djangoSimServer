#models.py 

from django.db import models
from django.utils import timezone

class CarOwners(models.Model):
    name = models.CharField(max_length=100)
    car_number = models.CharField(max_length=20)
    parking_slot_number = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'car_number': self.car_number,
            'parking_slot_number': self.parking_slot_number,
            'phone_number': self.phone_number,
        }

class ReceivedCall(models.Model):
    user = models.ForeignKey(CarOwners, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    @property
    def formatted_timestamp(self):
        # Convert datetime to the timezone you want
        datetime_in_ist = timezone.localtime(self.timestamp)
        # Format timestamp as string
        return datetime_in_ist.strftime('%Y-%m-%d %H:%M:%S')


class RecentLog(models.Model):
    ownerId = models.IntegerField()
    name = models.CharField(max_length=100)
    slot_no = models.CharField(max_length=10)
    car_no = models.CharField(max_length=20)
    datetime = models.DateTimeField(default=timezone.now)

    @property
    def formatted_date(self):
        # Format date as DD-MM-YYYY
        return self.datetime.strftime('%d-%m-%Y')

    @property
    def formatted_time(self):
        # Convert datetime to the timezone you want
        datetime_in_ist = timezone.localtime(self.datetime)
        # Format time in terms of AM/PM
        return datetime_in_ist.strftime('%I:%M %p')

    class Meta:
        ordering = ['-datetime']

class AllLogs(models.Model):
    ownerId = models.IntegerField()
    name = models.CharField(max_length=100)
    slot_no = models.CharField(max_length=100)
    car_no = models.CharField(max_length=100)
    datetime = models.DateTimeField(default=timezone.now)

    @property
    def formatted_date(self):
        # Format date as DD-MM-YYYY
        return self.datetime.strftime('%d-%m-%Y')

    @property
    def formatted_time(self):
        # Convert datetime to the timezone you want
        datetime_in_ist = timezone.localtime(self.datetime)
        # Format time in terms of AM/PM
        return datetime_in_ist.strftime('%I:%M %p')

    class Meta:
        ordering = ['-datetime']


class SMSTask(models.Model):
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)