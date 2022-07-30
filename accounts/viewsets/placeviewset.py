# from rest_framework import viewsets, status
# from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
# from rest_framework.decorators import action
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.response import Response
# from rest_framework import filters
# from accounts.permission import IsOwnerOrReadOnly
#
# from accounts.models import Place, PlaceImage, PlaceReview
#
# from accounts.serializers.place_register import PlaceRegisterSerializer, AddReviewSerializer
# from accounts.serializers.place_serializer import PlaceReviewSerializer, PlaceDetailSerializer, \
#                                                PlaceReviewSerializer
#
#
# class PlaceViewSet(viewsets.ModelViewSet):
#     """
#     A PlaceViewSet will provide API related to Add, View and Update.
#     """
#     model = Place
#     queryset = model.objects.all()
#     serializer_class = PlaceRegisterSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     http_method_names = ['get', 'post', 'patch']
#     filter_backends = [filters.SearchFilter]  # This will implement filter for search.
#     search_fields = ['name']  # Here we are selecting the field on which we want to field
#
#     def get_serializer_class(self):
#         """
#         Change serializer as based on action.
#         :return:
#         """
#         if self.action == 'retrieve':
#             return PlaceDetailSerializer
#         return super().get_serializer_class()
#
#     def get_permissions(self):
#         """
#         Change permission as based on action.
#         :return:
#         """
#         if self.action == 'update' or self.action == 'partial_update':
#             permission_classes = [IsOwnerOrReadOnly]
#         else:
#             permission_classes = [IsAuthenticatedOrReadOnly]
#         return [permission() for permission in permission_classes]
#
#
# class PlaceReviewViewset(viewsets.ModelViewSet):
#     model = PlaceReview
#     queryset = model.objects.all()
#     serializer_class = PlaceReviewSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     http_method_names = ['get', 'post', 'patch']
#
#     def get_serializer_class(self):
#         """
#         Send custom serializer based on action.
#         :return:
#         """
#         if self.action == 'create':
#             return AddReviewSerializer
#         elif self.action in ('retrieve', 'list'):
#             return PlaceReviewSerializer
#         elif self.action == 'list':
#             return PlaceReviewSerializer
#         return super().get_serializer_class()
#
#     @action(detail=True, methods=['post', 'get'])
#     def get_reviews(self, request, **kwargs):
#         """
#         Get review list on selected place based.
#         :param request:
#         :param kwargs:
#         :return:
#         """
#         reviews = PlaceReview.objects.filter(place_id=kwargs.get('pk'))
#         serializer = PlaceReviewSerializer(reviews, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
# # for filtering https://sunscrapers.com/blog/the-ultimate-tutorial-for-django-rest-framework-filtering-part-5/
