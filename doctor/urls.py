from django.urls import path
from doctor.views.login import DoctorLoginView
from doctor.views.animal import AnimalCreateView
from doctor.views.register import DoctorRegisterView
from doctor.views.villager import VillagerCreateView

urlpatterns = [
    path('register/', DoctorRegisterView.as_view(), name='doctor-register'),
    path('login/', DoctorLoginView.as_view(), name='doctor-login'),
    path('villager/add/', VillagerCreateView.as_view(), name='add-villager'),
    path('animal/add/', AnimalCreateView.as_view(), name='add-animal'),
]