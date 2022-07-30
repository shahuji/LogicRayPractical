# from rest_framework import serializers
#
# from accounts.models import Place, PlaceImage, PlaceReview
# from accounts.models import User
#
# __all__ = ['PlaceReviewSerializer', 'PlaceDetailSerializer', 'PlaceReviewSerializer']
#
#
# class ReviewSerializer(serializers.ModelSerializer):
#     """
#     This serializer will hep to send with PlaceDetailSerializer.
#     """
#
#     class Meta:
#         model = PlaceReview
#         fields = ['review', 'rating']
#
#
# class ImageSerializer(serializers.ModelSerializer):
#     """
#     This serializer will hep to send with PlaceDetailSerializer.
#     """
#
#     class Meta:
#         model = PlaceImage
#         fields = ['place_image']
#
#
# class PlaceDetailSerializer(serializers.ModelSerializer):
#     """
#     This serializer is for getting detail of perticular/single Place details.
#     """
#     place_image = ImageSerializer(many=True, read_only=True)
#     place_review = ReviewSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Place
#         fields = ['id', 'name', 'lattitude', 'longitude', 'total_review', 'avg_rate', 'about', 'total_review',
#                   'avg_rate', 'place_image', 'place_review']
#
#
# class PlaceReviewSerializer(serializers.ModelSerializer):
#     """
#     This will send review of place.
#     """
#
#     class Meta:
#         model = PlaceReview
#         fields = ['review', 'rating', 'place']
