from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.conf import settings
from .models import Account, Profile, Adress, EmailSubscribe, RandomNumber, AuthPhoneNumber
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
import json
import random
import requests

#oauth
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

#serializer
from .serializers import AccountSerializer, EmailSubscribeSerializer
from .serializers import AccountSerializer, MyTokenObtainPairSerializer
from .serializers import AccountEditSerializer, ProfileEditSerializer, AdressEditSerializer
from .serializers import AuthPhoneNumberSerializer

import logging

#token発行
from six import text_type

# cookiejwtのためのimport
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator

logging = logging.getLogger(__name__)

#認証時tokenを発行しセキュリティを高める
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.id) + text_type(timestamp) + text_type(user.email)
        )

# emailとpasswordを確認するためのapi

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class AccountRegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountRegisterConfirmation(generics.UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny, )

    # database内容を変更するためpostに変更
    # created_at時刻とフロント側で現在時刻を取得し差分が1日以上の場合には例外をraiseするようにする
    def update(self, request, *args, **kwargs):
        try:
            id = request.data['id']
            instance = Account.objects.get(id=id)
            instance.is_active = True
            instance.save(update_fields=["is_active"])
            data = {'message':'本登録が完了しました'}
            return Response(data, status=status.HTTP_200_OK)
        except:
            data = {'message':'本登録に失敗しました、Enclopedia運営にお問合せ下さい。'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
            

class AccountRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountEditSerializer

    def get(self, request):
        instance = get_object_or_404(self.queryset, id=request.user.id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        data = request.data
        instance = get_object_or_404(Account, id=request.user.id)
        instance.first_name = data['first_name']
        instance.last_name = data['last_name']
        instance.username = data['username']
        instance.save()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        instance = get_object_or_404(Account, id=request.user.id)
        instance.delete()
        data = {'message': 'アカウントを削除しました'}
        return Response(data, status=status.HTTP_200_OK)

#googleを利用したoauthlogin
class GoogleLoginView(SocialLoginView):
    authentication_classes = []  # disable authentication
    adapter_class = GoogleOAuth2Adapter
    callback_url = "https://www.enclopedia-official.com"  # サーバ切り替え時に変更
    client_class = OAuth2Client


class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileEditSerializer

    def get(self, request):
        instance = get_object_or_404(self.queryset, user=request.user)
        serializer = self.serializer_class(
            instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Profile, user=request.user)
        instance.gender = request.data['gender']
        instance.birth_day = request.data['birth_day']
        instance.img.delete()
        instance.img = request.data['img']
        instance.save()
        serializer = self.serializer_class(
            instance, partial=True)
        return Response(serializer.data)

# This function is to get or update or delete Adress model
class AdressRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Adress.objects.all()
    serializer_class = AdressEditSerializer

    def get(self, request):
        instance = get_object_or_404(self.queryset, user=request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = Adress.objects.select_related('user').get(user=request.user)
        data = request.data
        instance.country = data['country']
        instance.prefecture = data['prefecture']
        instance.region = data['region']
        instance.address = data['address']
        instance.building_name = data['building_name']
        instance.postalcode = data['postalcode']
        instance.save()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, user=request.user)
            instance.delete()
            message = 'アドレスを削除しました。'
            return Response(message, status=status.HTTP_200_OK)
        except:
            message = '削除に失敗しました。'
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

#機密情報updateの際パスワードとemailを取得して確認する必要性がある
class UserConfirmView(APIView):
    def post(self, request):
        data = request.data
        user = request.user
        password = data['password']
        new_password = data['new_password']
        
        auth_result = authenticate(
            email = user.email,
            password = password
        )
        

        if auth_result:
            user.set_password(new_password)
            user.save()
            data={'message':'パスワードの変更が完了しました。'}
            return Response(data, status=status.HTTP_200_OK)
        else:
            message = {'message': '入力したパスワードは認証できません。'}
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)

class EmailUpdateView(generics.UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountEditSerializer

    def update(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        password = data['password']
        email = data['email']
        new_email = data['new_email']

        auth_result = authenticate(
            email = email,
            password = password
        )
        if auth_result:
            user.email = new_email
            user.save()
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            message = {'message': '入力したEメールあるいはパスワードが正しくありません'}
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)
#suppressionsを利用しemailを特定の購読グループに追加する
class SendgridRecipientView(APIView):
    def post(self, request):
        data = request.data
        try:
            secret = settings.SENDGRID_API_KEY
            #header情報を富要する
            header = {'Content-type':'application/json', 'Authorization':'Bearer ' + secret}
            #sendgridのメールリストに単一のメールアドレスを追加する
            url = 'https://api.sendgrid.com/v3/contactdb/recipients'
            data = [{
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
            }]
            response = requests.post(url, data=json.dumps(data), headers=header,)
            return Response(response, status=status.HTTP_200_OK)
        except :
            message = {'message':'メール配信リスト登録が失敗しました。'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
    
    
    #group unsubscriptionに登録と削除でmarktingメールを送信するかどうか決定。
    def delete(self, reqeust):
        #sendgrid 配信リストからuerのemailを削除するためのapiを叩く
        try:
            secret = settings.SENDGRID_API_KEY
            recipient_id = ''
            header = {'Content-type':'application/json', 'Authorization':'Bearer ' + secret}
            url = 'https://api.sendgrid.com/v3/contactdb/recipients/' + recipient_id
            response = requests.delete(url, headers=header)
            return Response(response, status.HTTP_200_OK)
        except:
            message = {'message':'メール配信リストから削除しました。'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

#日購読グループへの登録を送るようにする
class SendgridSuppressionsView(APIView):
    #マーケティングメールの配信をリストに追加すると停止する
    def post(self, request):
        try:
            email = request.data['email']
            secret = settings.SENDGRID_API_KEY
            header = {'Content-type':'application/json', 'Authorization':'Bearer ' + secret}

            url = 'https://api.sendgrid.com/v3/asm/groups/{}/suppressions'.format('30160')
            data = {
                "recipient_emails":[
                    email
                ]
            }
            response = requests.post(url, headers=header, data=json.dumps(data))
            return Response(response, status=status.HTTP_200_OK)

        except:
            message = {'message':'メール配信リストへの登録に失敗しました。'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
            
    #配信停止リストから削除することで配信を再度開始する
    def delete(self, request, *args, **kwargs):
        email  = request.GET['mail']
        try:
            secret = settings.SENDGRID_API_KEY
            header = {'Content-type':'application/json', 'Authorization':'Bearer ' + secret}
            url = 'https://api.sendgrid.com/v3/asm/groups/{}/suppressions/{}'.format('30160', email)
            response = requests.delete(url, headers=header)
            return Response(response, status=status.HTTP_200_OK)
        except:
            message = {'message':'メール配信リストからの削除に失敗しました。'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

#アカウント作成をすると自動的に登録されるようになっている
#マーケティング用のメール購読が有効かどうか
class EmailSubscribeView(generics.RetrieveUpdateAPIView):
    queryset = EmailSubscribe.objects.select_related('account').all()
    serializer_class = EmailSubscribeSerializer
    lookup_field = "pk"

    def get(self, request):
        subscribe = get_object_or_404(EmailSubscribe, user=request.user)
        serializer = self.serializer_class(subscribe)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(EmailSubscribe, user=request.user)
        instance.is_active = request.data['is_active']
        instance.save()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

#phone_numberを変更認証


class PhoneNumberUpdateAPIView(APIView):
    #こちらに問い合わせがあった場合には認証コードを発行しゆう期限内で認証情報を保持し続ける必要がある
    #同一番号を発行しないように有効期限は5分間とする
    def generate_number(self):
        number = random.randrange(1,9999)
        return number

    def post(self, request, *args, **kwargs):
        #作成したtableから生成したidを
            number = self.generate_number()
            auth_number = RandomNumber.objects.get(id=number)
            #番号が重複しないようにフィルターを✖️必要がある
            #AuthPhoneNumberが作成されてからシグナルで有効時間経過後に削除するプログラムを作成する

            if AuthPhoneNumber.objects.filter(random_number=auth_number, user=request.user).exists():
                number = self.generate_number()
                auth_number = RandomNumber.objects.get(id=number)
                instance = AuthPhoneNumber.objects.create(random_number=auth_number, user=request.user)
                serializer = AuthPhoneNumberSerializer(instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                instance = AuthPhoneNumber.objects.create(random_number=auth_number, user=request.user)
                serializer = AuthPhoneNumberSerializer(instance)
                return Response(serializer.data)

    
    def put(self, request, *args, **kwargs):
        try:
            phone_number = request.data['phone_number']
            account = get_object_or_404(Account, id=request.user.id)
            account.phone_number = phone_number
            account.save()
            serializer = AccountSerializer(account)
            auth_number = AuthPhoneNumber.objects.filter(user=request.user)
            auth_number.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

import time
class AuthenticationNumberView(APIView):
    def post(self, request, *args, **kwargs):
        number = request.data['authentication_number']
        authentication = get_object_or_404(AuthPhoneNumber, random_number__number=number, user=request.user)
        #現在の時刻と認証コード発行時間から5以上経過している場合はエラーを返し削除するようにする
        if (authentication.created_at.timestamp() - time.time()) > 300:
            data = {"message": "５分以上経過しています、もう一度認証コードを取得の上変更を行なって下さい"}
            authentication.delete()
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(True, status=status.HTTP_200_OK)

