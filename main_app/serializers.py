from django.db import models
from rest_framework.serializers import ModelSerializer
from main_app.models import Progress_bar


class Main_app_serializers(ModelSerializer):
    class Meta:
        model = Progress_bar
        fields = '__all__'