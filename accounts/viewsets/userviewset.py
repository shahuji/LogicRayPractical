from django.contrib.auth import login, logout
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
import random

from rest_framework.authtoken.models import Token
from accounts.models import Product, Order, OrderList

from accounts.serializers.register import RegisterSerializer
from accounts.serializers.auth_serializer import LoginSerializer, OTPLogin, UserProfileSerialization
from accounts.serializers.product_serializer import ProductListSerializer, OrderProductSerializer, OrderDetailSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    A UserViewSet will provide API related to Login, Logout.
    """
    model = User
    queryset = model.objects.all().filter(is_active=True)
    serializer_class = UserProfileSerialization
    http_method_names = ['get', 'post', 'patch']
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsOwnerOrReadOnly]

    @action(detail=False, methods=['post'], serializer_class=RegisterSerializer)
    def register(self, request, *args, **kwargs):
        """
        This method will valid login credentials.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # # checking is user token already exists
        # Token.objects.create(user=user)
        # token = Token.objects.get(user=user)

        user_serializer = UserProfileSerialization(user)
        data = user_serializer.data
        # data['token'] = token.key
        # print("TOKEN = " + token.key)
        return Response({'code': '1', 'message': 'Register Sucessfully!!!', 'data': data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], serializer_class=LoginSerializer)
    def login(self, request, *args, **kwargs):
        """
        This method will valid login credentials and generate token.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.otp = random.randint(1000, 9999)
        user.save()
        print("User OTP: ", user.otp)

        # login(request, user)
        #
        # # checking is user token already exists
        # token = Token.objects.filter(user=user)
        # if not token:
        #     Token.objects.create(user=user)
        # token = Token.objects.get(user=user)
        # # print(token.key)
        # user_serializer = UserProfileSerialization(user)
        # data = dict()
        # data['data'] = user_serializer.data
        # data['data']['token'] = token.key
        # print(data)
        return Response({'code': '1', 'message': 'OTP send succesfully', "data": {"id": user.id}}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], serializer_class=OTPLogin)
    def otp(self, request, *args, **kwargs):
        """
        This method will valid login credentials and generate token.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.otp = ""
        user.save()

        login(request, user)

        # checking is user token already exists
        token = Token.objects.filter(user=user)
        if not token:
            Token.objects.create(user=user)
        token = Token.objects.get(user=user)
        # print(token.key)
        user_serializer = UserProfileSerialization(user)
        data = dict()
        data['data'] = user_serializer.data
        data['data']['token'] = token.key
        print(data)
        return Response({'code': '1', 'message': 'Succesfully Login.', "data": {**data}},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def logout(self, request):
        """
        This method will log out signed user and delete token.
        :param request:
        :return:
        """
        # user = User.objects.get(id=request.user.id)
        token = Token.objects.get(user=request.user.id)
        # print(user)  # Get Login User Details
        # print("TOKEN = " + token.key)  # Get Login User Token
        Token.objects.get(user=request.user.id).delete()
        logout(request)
        return Response({'code': '1', 'message': 'Sucessfully Logout!'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], serializer_class=UserProfileSerialization,
            permission_classes=[IsAuthenticated])
    def get_user_profile(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response({'code': '1', 'message': 'Succesfully User Details!!!!', 'data': serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], serializer_class=ProductListSerializer,
            permission_classes=[IsAuthenticated])
    def product_list(self, request, *args, **kwargs):
        serializer = self.serializer_class(Product.objects.filter(is_active=True), many=True)
        return Response({'code': '1', 'message': 'Product list get successfully', 'data': serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], serializer_class=OrderProductSerializer)
    def orders(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request, 'view': self})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response({'code': '1', 'message': 'Succesfully Login.', "data": {**OrderDetailSerializer(order).data}},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], serializer_class=OrderProductSerializer)
    def order(self, request, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs.get('pk'), is_active=True)
        order_list = OrderDetailSerializer(order, context={'request': request, 'view': self})
        return Response({'code': '1', 'message': 'Succesfully Login.', "data": {**order_list.data}},
                        status=status.HTTP_200_OK)
