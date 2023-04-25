from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from user.models import Profile

import environ
import openai

env = environ.Env()
CHATGPT_SECRET_API = env("CHATGPT_API_KEY")
openai.api_key = CHATGPT_SECRET_API

# 性別,身長,体重
# promptの文章再生に関してこちらで確認する
# 必要な情報の洗い出しそれを英文にする必要がある
# それぞれの趣旨に合わせた  
# 素材
# 色 お気に入りの色から
# サイズ感
# スタイル
# インナー、トップス、ボトム、アクセサリー、靴を詳細に決定するためには？
# 自分でどこまで決めたいかそれとも全てお任せでコードを組んで欲しいのか考える
# closetからどんな洋服を保存しているのかチェック。
# 言語化する必要がある
# 言語化したアイテムをchatgptapiのembeddingsを使用してクラスタリングする
# 意思を介在させるには？
# レイヤニングについて考える
# 記入した色からカラーパレットを作成する
# detailを詳細に説明する
# まずスタイルによってまずスタイルによって
# 適切なサイズ感のものを敵強する必要がある
# 適さない表現も存在するのでどのようにする必要がある
# ウエストについて
# 体のフィット感についての好み

class CreateImageView(APIView):
    def post(self, request):
        data = request.data
        silhouette = data['silhouette']
        brand = data['brand']
        style = data['style']
        color = data['color']
        material = data['material']
        situation = data['situation']
        #promptを作成
        prompt = "Desired 170cm 45kg female full body styling, image(Season: Spring, Scene: party,  Age: 20s, style: minimal style, favorite color: black, Tops: oversize tailored jacket, Bottom: Flounce Detail Midi Skirt, Shoes: black ballet shoes, socks:flower-patterned socks, Favorite Brand: simone rocha)"

        #profile情報から身体に関しての情報を取得する    
        prompt = "Desired 170cm 45kg female full body styling, image(Season: Spring, Scene: party,  Age: 20s, style: minimal style, favorite color: black, Tops: oversize tailored jacket, Bottom: Flounce Detail Midi Skirt, Shoes: black ballet shoes, socks:flower-patterned socks, Favorite Brand: simone rocha)"
        response = openai.Image.create(
            prompt = prompt,
            n = 1,
            size="1024x1024"
        )
        #生成した画像は保存するようにする
        return Response(response['data'], status=status.HTTP_200_OK)