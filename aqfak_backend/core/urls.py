from django.urls import path
from . import views

urlpatterns = [
    path('list_create_crop/',views.list_create_crop),
    # path('getcrop_details/',views.getcrop_details),
    path('retreive_update_delete_crop/<str:id>/',views.retrieve_update_delete_crop),
    path('create_crop_sensor_data/<str:id>/',views.create_crop_sensor_data),
]