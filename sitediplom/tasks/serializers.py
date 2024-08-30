from rest_framework import serializers
from .models import *

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'


class FavoriteTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteTask
        fields = '__all__'
