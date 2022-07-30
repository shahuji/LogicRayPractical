from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
import random
# from account.utils import GenerateOtp

from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    A RegisterSerializer is for API of user registartion.
    """
    # error_messages={'required': 'Email field is required1.',
    #                                                    'blank': 'Email field must not be blank1.'
    #                                                    }
    username = serializers.CharField(required=True, max_length=64,
                                     error_messages={'required': 'Username field is required.',
                                                     'blank': 'Username field must not be blank.'
                                                     })
    email = serializers.EmailField(required=True, max_length=128,
                                     error_messages={'required': 'Email field is required.',
                                                     'blank': 'Email field must not be blank.'
                                                     })
    name = serializers.CharField(required=True, max_length=16,
                                     error_messages={'required': 'Name field is required.',
                                                     'blank': 'Name field must not be blank.'
                                                     })
    phone = serializers.CharField(required=True, max_length=12,
                                     error_messages={'required': 'Phone field is required.',
                                                     'blank': 'Phone field must not be blank.'
                                                     })
    password = serializers.CharField(required=True,
                                     error_messages={'required': 'Password field is required.',
                                                     'blank': 'Password field must not be blank.'
                                                     })

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'phone', 'password']

    def validate(self, attrs):
        """
        This method will validate login credentials and also check user is active or not.
        :param attrs:
        :return:
        """
        password = attrs.get('password')
        username = attrs.get('username')
        email = attrs.get('email')
        phone = attrs.get('phone')

        if username and User.objects.filter(username=username, is_active=True):
            raise AuthenticationFailed('Username is already registered.')

        if email and User.objects.filter(email=email, is_active=True):
            raise AuthenticationFailed('Email is already registered.')

        if phone and User.objects.filter(phone=phone, is_active=True):
            raise AuthenticationFailed('Phone is already registered.')
        # if signup_type == 1:
        #     elif not password:
        #         raise AuthenticationFailed('Password must required, try again!!!')
        #     elif not email:
        #         raise AuthenticationFailed('Email must required, try again!!!')
        # elif signup_type in (2, 3):
        #     if not social_id:
        #         raise AuthenticationFailed('Social-Id is required')
        #     elif not email:
        #         raise AuthenticationFailed('Email must required, try again!!!')

        return super().validate(attrs)

    def create(self, validated_data):
        # print(validated_data)
        user = super().create(validated_data)

        user.set_password(validated_data['password'])
        user.save()
        return user
