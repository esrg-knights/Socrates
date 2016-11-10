from django.contrib.auth.models import User
from rest_framework import serializers

from account.models import DetailsModel
from achievements.models import Achievement, Game, AchievementGet
from dining.models import DiningList, DiningParticipation, DiningComment


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializes a users details
    """
    class Meta:
        model = DetailsModel
        fields = ('id', 'allergies', 'rather_nots')


class SimpleUserSerializer(serializers.ModelSerializer):
    """
    Serializes a user without details
    """
    class Meta:
        model = User
        fields = ('id', 'username')


class UserWithProfile(serializers.ModelSerializer):
    """
    Serialize a user with details
    """
    details = UserDetailsSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'details')


class DiningCommentSerializer(serializers.ModelSerializer):
    """
    Serialize a comment on a dinnerlist
    """
    user = SimpleUserSerializer(many=False, read_only=False)

    class Meta:
        model = DiningComment
        fields = ('user', 'body', 'date_posted')


class DiningParticipationSerializer(serializers.ModelSerializer):
    """
    Serialize a participation on a dinnerlist
    """
    user = UserWithProfile(many=False, read_only=True)

    class Meta:
        model = DiningParticipation
        fields = ('work_dishes', 'work_cook', 'work_groceries', 'user')


class DinnerListSerializer(serializers.ModelSerializer):
    """
    Serializes a dinner list
    """
    participations = DiningParticipationSerializer(many=True, read_only=True)
    comments = DiningCommentSerializer(many=True, read_only=True)

    class Meta:
        model = DiningList
        fields = ('id', 'relevant_date', 'owner', 'participations', 'comments')


class SimpleAchievementGetSerializer(serializers.ModelSerializer):
    """
    Simple serializer only using FK relations
    """
    class Meta:
        model = AchievementGet
        fields = ("user", "awarded_by", "score", "date_achieved", "achievement")


class AdvancedAchievementGetSerializer(serializers.ModelSerializer):
    """
    Advanced achievement get serializer, loading the users too
    """
    user = UserWithProfile(many=False, read_only=True)
    awarded_by = UserWithProfile(many=False, read_only=True)

    class Meta:
        model = AchievementGet
        fields = ("id", "user", "awarded_by", "date_achieved", "score")


class GameSerializer(serializers.ModelSerializer):
    """
    Serializes a game
    """
    class Meta:
        model = Game
        fields = ("id", "name", "image")


class AchievementSerializer(serializers.ModelSerializer):
    """
    Serializes an achievement, loading nested objects too
    """
    related_game = GameSerializer(many=False, read_only=True)
    gets = AdvancedAchievementGetSerializer(many=True, read_only=True)

    class Meta:
        model = Achievement
        fields = ("id", "name", "description", "image", "date_created", "related_game", "gets")
