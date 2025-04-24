import re
from rest_framework import serializers
from .models import Doctor, Villager, Animal
from django.contrib.auth.hashers import make_password

class DoctorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'phone_number', 'address', 'email', 'village_assign', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_phone_number(self, value):
        # Check if it's exactly 10 digits and only numeric
        if not re.fullmatch(r'\d{10}', value):
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        if Doctor.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number is already registered.")
        return value

    def validate_email(self, value):
        # Check if email already exists
        if Doctor.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def validate_password(self, value):
        # Check password strength: min 8 chars, must include at least one letter and one digit
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Za-z]', value) or not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one letter and one number.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    
class VillagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Villager
        fields = '__all__'

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'
