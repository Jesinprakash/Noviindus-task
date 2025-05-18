from rest_framework import serializers

from rest_framework import serializers
from taskapp.models import Task,User

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        # read_only_fields = ['assigned_to']

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']


class UserSerializer(serializers.ModelSerializer):

    password1=serializers.CharField(write_only=True)

    password2=serializers.CharField(write_only=True)

    password=serializers.CharField(read_only=True)


    class Meta:

        model=User

        fields=["username","email","role","password1","password2","password"]

    def validate(self, data):
        if data.get("password1") != data.get("password2"):

            raise serializers.ValidationError("password mismatch")
        return data

    def create(self, validated_data):

        password1=validated_data.pop("password1")

        password2=validated_data.pop("password2")

        return User.objects.create_user(**validated_data,password=password1)
