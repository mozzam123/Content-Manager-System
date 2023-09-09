from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator, EmailValidator
from .models import CustomUser, ContentItem

class CustomUserSerializer(serializers.ModelSerializer):
    # Password field with custom validation
    password = serializers.CharField(write_only=True, validators=[
        validate_password,
        RegexValidator(
            regex='^(?=.*[a-z])(?=.*[A-Z]).{8,}$',
            message='Password must be at least 8 characters long and contain at least one uppercase and one lowercase letter.'
        )
    ])

    # Email field with email format validation
    email = serializers.EmailField(validators=[EmailValidator(message="Enter a valid email address.")])

    # Phone number field with validation
    phone = serializers.CharField(validators=[
        RegexValidator(
            regex='^\d{10}$',  # Customize the regex as per your requirements
            message='Phone number must be 10 digits long.'
        )
    ])

    # Pincode field with validation
    pincode = serializers.CharField(validators=[
        RegexValidator(
            regex='^\d{6}$',  # Customize the regex as per your requirements
            message='Pincode should be 6 digits only.'
        )
    ])

    class Meta:
        model = CustomUser
        fields = '__all__'

class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentItem
        fields = ['title', 'body']
