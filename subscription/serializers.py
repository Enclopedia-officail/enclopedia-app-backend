from rest_framework import serializers
from .models import StripeAccount

class StripeSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StripeAccount
        fields = ['is_active', 'plan', 'start_date', 'update_date', 'cancel_date']
