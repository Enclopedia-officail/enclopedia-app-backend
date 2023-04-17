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
openai.api_key = CHATGPT_SECRET_API

#性別,身長,体重
#promptの文章再生に関してこちらで確認する
#必要な情報の洗い出しそれを英文にする必要がある
#それぞれの趣旨に合わせた  
# 素材
# 色
# サイズ感
#      
class CreateImageView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        #promptを作成
        prompt = 'Generate an image of a Caucasian female model wearing a layered styling with a tight silhouette like Comme des Garcons, with black gathers on a white background to make her whole body and face look beautiful.'
        response = openai.Image.create(
            prompt = prompt,
            n = 1,
            size="1024x1024"
        )   
        return Response(response['data'], status=status.HTTP_200_OK)
