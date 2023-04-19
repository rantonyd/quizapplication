from rest_framework import serializers
from quiz.models import Category,Questions,Answers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']


class CategorySerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    is_active=serializers.CharField(read_only=True)
    class Meta:
        model=Category
        fields="__all__"

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)




class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Answers
        fields=["options","is_correct"]

class QuestionSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    category=serializers.CharField(read_only=True)
    options=AnswerSerializer(many=True)
    
    class Meta:
        model=Questions
        fields=["id","category","mode","mark","question","options"]
