from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

import environ
import openai

env = environ.Env()
CHATGPT_SECRET_API = env("CHATGPT_API_KEY")

#promptをどのように編集するかを考える必要がある
#promptの文章再生に関してこちらで確認する
#必要な情報の洗い出しそれを英文にする必要がある
class CreateImageView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        data = request.data
        #promptを作成
        prompt = data['prompt']
        response = openai.Image.create(
            prompt = prompt,
            n = 1,
            size="1024x1024"
        )   
        return Response(response['data'], status=status.HTTP_200_OK)
