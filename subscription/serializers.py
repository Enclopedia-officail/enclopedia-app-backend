from rest_framework import serializers
from .models import StripeAccount, Payment
from user.serializers import AccountSerializer


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['id', 'payment_method', 'payment_id']

class StripeSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StripeAccount
        fields = ['is_active', 'plan', 'start_date', 'update_date', 'cancel_date']
