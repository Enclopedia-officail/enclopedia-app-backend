from rest_framework import serializers
from .models import InvitationCode

class InvitationCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvitationCode
        fields = ['code']
