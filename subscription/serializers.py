from rest_framework import serializers
from .models import StripeAccount
from user.serializers import AccountSerializer

class StripeSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StripeAccount
        fields = ['is_active', 'plan', 'start_date', 'update_date', 'cancel_date']

class PaymentSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)

    class Meta:
        fields = ['id', 'user', 'payment_method', 'payment_id', 'created_at']