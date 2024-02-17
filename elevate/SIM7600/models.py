# models.py

from django.db import models

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
