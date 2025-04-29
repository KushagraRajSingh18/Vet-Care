import re
from rest_framework import serializers
from .models import Doctor, Villager, Animal
from django.contrib.auth.hashers import make_password

class DoctorRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'phone_number', 'address', 'email', 'village_assign', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_phone_number(self, value):
        # Normalize phone number (remove +91 if present)
        if value.startswith('+91'):
            value = value[3:]

        if not re.fullmatch(r'[6-9]\d{9}', value):
            raise serializers.ValidationError("Phone number must start with 6/7/8/9 and be 10 digits long.")

        normalized_number = value
        if Doctor.objects.filter(phone_number__endswith=normalized_number).exists():
            raise serializers.ValidationError("Phone number is already registered.")

        return '+91' + normalized_number

    def validate_email(self, value):
        value = value.lower()
        if Doctor.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Password and Confirm Password do not match."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return Doctor.objects.create(**validated_data)

class VillagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Villager
        fields = '__all__'

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'
