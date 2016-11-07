from django.contrib.auth.models import User
from rest_framework import serializers

from account.models import DetailsModel
from dining.models import DiningList, DiningParticipation, DiningComment


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailsModel
        fields = ('id', 'allergies', 'rather_nots')


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class UserWithProfile(serializers.ModelSerializer):
    details = UserDetailsSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'details')


class DiningCommentSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(many=False, read_only=False)

    class Meta:
        model = DiningComment
        fields = ('user', 'body', 'date_posted')


class DiningParticipationSerializer(serializers.ModelSerializer):
    user = UserWithProfile(many=False, read_only=True)

    class Meta:
        model = DiningParticipation
        fields = ('work_dishes', 'work_cook', 'work_groceries', 'user')


class DinnerListSerializer(serializers.ModelSerializer):
    participations = DiningParticipationSerializer(many=True, read_only=True)
    comments = DiningCommentSerializer(many=True, read_only=True)

    class Meta:
        model = DiningList
        fields = ('id', 'relevant_date', 'owner', 'participations', 'comments')
