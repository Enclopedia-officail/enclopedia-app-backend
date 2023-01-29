from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
import environ
#google analyticsでログイン
#access tokenを発行するのだがこの

env = environ.Env()

class GoogleLoginView(SocialLoginView):
    authentication_classes = []
    adapter_class = GoogleOAuth2Adapter
    callback_url = env('FRONTEND_URL')
    client_class = OAuth2Client

@csrf_exempt
class RefreshTokenView(APIView):

    def post(self, request, *args, **kwargs):
        request.data._mutable = True
