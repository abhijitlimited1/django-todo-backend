from rest_framework import serializers
from .models import RegisterUser,Tasks

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields =['id','first_name','last_name','email','password']
        extra_kwargs = {
            'password': {'write_only': True},
        }



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id','todo','completed']