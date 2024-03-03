# sim7600/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('make_call', views.make_call, name='make_call'),
    path('send_text_message', views.send_text_message, name='send_text_message'),
    path('new_car_owner', views.new_car_owner, name='new_car_owner'),
    path('get_all_car_owner', views.get_all_car_owners, name='get_all_car_owner'),
    path('get_car_owner_detail',views.get_car_owner_detail,name='get_car_owner_detail'),
    path('update_owner_data', views.update_owner_data, name='update_owner_data'),
    path('delete_owner_data', views.delete_owner_data, name='delete_owner_data'),
    path('handle_incoming_call', views.handle_incoming_call, name='handle_incoming_call'),
    path('get_all_received_call',views.get_all_received_call,name='get_all_received_call'),
]
