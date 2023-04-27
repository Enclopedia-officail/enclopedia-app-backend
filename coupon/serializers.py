from rest_framework import serializers
from .models import Coupon, InvitationCode, Issuing, Invitation

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'type', 'amount_off', 'created_at', 'currency', 'duration', 'duration_in_month', 'duration_in_times', 'max_redemptions', 'name', 'percent_off', 'times_redeemed', 'redeem_by']

class InvitationCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvitationCode
        fields = ['code']

class IssuingSerializer(serializers.ModelSerializer):
    coupon = CouponSerializer(read_only=True)
    class Meta:
        model = Issuing
        fields = ['coupon', 'is_used', 'expiration']

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['phone_number']