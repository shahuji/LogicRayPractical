from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
# from accounts.utils import Util, GenerateOtp

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth import get_user_model

User = get_user_model()

__all__ = ['LoginSerializer', 'OTPLogin', 'UserProfileSerialization']


class LoginSerializer(serializers.ModelSerializer):
    """
    A LoginSerializers is for API of login user authentication, verified by email and social_id.
    """
    email = serializers.EmailField(max_length=128, required=True,
                                   error_messages={'required': 'Email field is required.',
                                                   'blank': 'Email field must not be blank.'
                                                   })
    password = serializers.CharField(max_length=64, required=True, write_only=True,
                                     error_messages={'required': 'Password field is required.',
                                                     'blank': 'Password field must not be blank.'
                                                     })

    class Meta:
        model = User
        fields = ['email', 'password', ]

    def validate(self, attrs):
        """
        This method will validate login credentials and also check user is active or not.
        :param attrs: It contains signup_type, social_id, email, password.
        :return: And return validate credentials of login.
        """
        email = attrs.get('email')
        password = attrs.get('password')
        user = User.objects.get(email=email)
        if not user:
            raise AuthenticationFailed('User not found.')

        user = authenticate(username=user.username, password=password)
        if not user:
            raise AuthenticationFailed('Invalid password.')
        if user.is_active == 0:
            raise AuthenticationFailed('Acount is disabled, Contact ADMIN.')
        attrs['user'] = user
        return attrs


class OTPLogin(serializers.ModelSerializer):
    """
    Reset Password Serializer will work for resetting password.
    """
    id = serializers.IntegerField(required=True,
                                   error_messages={'required': 'Id field is required.',
                                                   'blank': 'Id field must not be blank.'})
    otp = serializers.CharField(max_length=4, required=True,
                                   error_messages={'required': 'OTP field is required.',
                                                   'blank': 'OTP field must not be blank.'})

    class Meta:
        model = User
        fields = ['id', 'otp']

    def validate(self, data):
        id = data['id']
        OTP = data['otp']
        user = User.objects.get(id=id, is_active=True)

        if not user:
            raise serializers.ValidationError('Id is invalid.')
        elif user.otp != OTP:
            raise serializers.ValidationError('Please enter valid OTP')
        data['user'] = user

        return data


class UserProfileSerialization(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'username', 'phone']
        read_only_fields = ['id', 'email', 'name', 'username', 'phone']
