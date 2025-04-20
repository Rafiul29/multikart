from rest_framework import serializers
from .models import CustomUser
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password', 'confirm_password']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Validate if password matches confirm password
        if password != confirm_password:
            raise serializers.ValidationError({'password': "Password don't match."})

        # Validate password strength (must contain at least one uppercase letter, lowercase letter, digit, symbol, and be at least 8 characters long)
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()-+]).{8,}$', password):
            raise serializers.ValidationError({
                "password": "This password must contain at least 8 characters, one uppercase letter, one lowercase letter, one digit, and one symbol."
            })

        # Validate if email already exists
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': "Email already exists."})

        return data

    def save(self, **kwargs):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']

        user = CustomUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        return user


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email','first_name','last_name'] 