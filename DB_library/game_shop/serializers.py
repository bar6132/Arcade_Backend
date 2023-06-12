from rest_framework import serializers
from .models import Game, UserProfile, User, ContactMsg, Message


class ContactMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMsg
        fields = '__all__'

    def create(self, validated_data):
        validated_data['status'] = 'in_progress'
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
