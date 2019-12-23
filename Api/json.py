from.models import user
from rest_framework import serializers

class json_user (serializers.ModelSerializer):
    class Meta:
        model=user
        fields=['id','Name','Mobile_Number']