from gettext import install
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account, Profile, Adress, EmailSubscribe
from rest_framework import status
from rest_framework.response import Response
from django.core import exceptions
import logging

# This function is to issue jwt toke  when user login

# ログインが認証エラーになっている状態、signalには原因はない

logging = logging.getLogger(__name__)

# cookie認証によるserializre


class MyTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = ClientInfoSerializer(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data


class ClientInfoSerializer(serializers.ModelSerializer):

    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        fields = ('first_name', 'last_name',
                  'is_active', 'username', )
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = AccountSerializer(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data


class AccountSerializer(serializers.ModelSerializer):

    token = serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField()

    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name',
                  'is_active', 'username', 'phone_number', 'email', 'password', 'token')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""

        res = Account.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user = Account.objects.get(email=res)
        return user

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token)


class AccountEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'username', 'email')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.save(update_fields=["first_name"])
        return instance


class UserSerializerWithToken(AccountSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        fields = ['id', '_id', 'first_name', 'last_name',
                  'username',  'email', 'password', 'token']
        extra_kwargs = {'password': {'min_length': 8}}

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token)

    def get__id(self, obj):
        return obj.id

# プロフィール情報更新


class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['gender', 'birth_day', 'img', ]
# reviewprofile serializer


class ProfileReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['img']

# アドレス情報更新

#
class AdressEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Adress
        fields = ['id', 'country', 'prefecture',
                  'region', 'address', 'building_name', 'postalcode']



# profiledataをreviewに結合させるため


class ReviewUserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        fields = ['username', 'profile']

    def get_profile(self, obj):
        profile = Profile.objects.get(user=obj)
        serializer = ProfileReviewSerializer(profile)
        return serializer.data['img']

class EmailSubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailSubscribe
        fields = ['is_active']

from .models import RandomNumber, AuthPhoneNumber
class RandomNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = RandomNumber
        fields = ['number']

class AuthPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthPhoneNumber
        fields = ['created_at']