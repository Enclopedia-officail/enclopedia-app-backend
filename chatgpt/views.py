from django.shortcuts import render
from rest_framework.permissions import AllowAny
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from user.models import Profile

import environ
import datetime
import openai
import deepl
import json

env = environ.Env()
DEEPL_SECRET_KEY = env('DEEPL_SECRET_KEY')
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
# 全てのコーデは網羅しきれない

#作成された画像はs3に保存

season = {
    1 : 'winter',
    2 : 'winter',
    3 : 'spring',
    4 : 'spring',
    5 : 'spring',
    6 : 'summer',
    7 : 'summer',
    8 : 'summer',
    9 : 'autumn',
    10 : 'autumn',
    11 : 'autumn',
    12 : 'winter'
}

def get_season():
    now = datetime.datetime.now()
    month = now.month
    data = season[int(month)]
    return data

def translate(content):
    translator = deepl.Translator(DEEPL_SECRET_KEY)
    result = translator.translate_text(content, target_lang="EN-US")
    print(result.text)
    return result.text


class CreateImageView(APIView):
    permission_classes = (AllowAny,)
    #生成した画像からどのように洋服をおすすめするか
    def post(self, request):
        data = request.data
        age = data['age']
        gender = data['gender']
        height = data['height']
        weight = data['weight']
        size = data['size']
        silhouette  = data['silhouette']
        brand = data['brand']
        style = data['style']
        color = data['color']
        material = data['material']
        situation = data['situation']
        season = get_season()
        #deepl
        content = "好きな色は{color}、服のシルエットは{silhouette}、好きなスタイルは{style}、好きなブランドは{brand}、服を着用するシーンは{situation}、好みの素材は{material}、身長は{height}cm、体重は{weight}kg、性別は{gender}、季節は{season}、以下の情報をもとにスタイリングを作成しデザインやディテールまで詳細に記載したアイテムについて他の文章は必要ないので{{tops:"", bottoms:"", inner:"",shoes:"",accessory:""}}のJSON形式だけで返して尚アイテムに関しては情報をもとにtops(シャツ、ポロシャツ、ブラウス、カーディーガン、ニット、チュニック、ワンピース、ジャケット、コートなど）、\
                   bottoms(デニム、スラックス、スカートなど）例に示したアイテムだけではなく考えられる全てのアイテムから情報に適したアイテムを選択すること。カラーに関しては好きな色の{color}を主体としつつ合うカラーパレットでスタイリングを組むこと。前の返答と同様の形式でjson形式の文章のみ返して".format(
            color=color,silhouette=silhouette,style=style,brand=brand,situation=situation,material=material, height=height,weight=weight,gender=gender,season=season
        )
        
        #上記の文章を翻訳する
        result = translate(content)

        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {
                    "role": "assistant",
                    "content": 
                    str({
                    "tops": "黒いビッグサイズのモードスタイルブラウス、立体的なディテールとレイヤードデザインが特徴",
                    "bottoms": "ワイドレッグの黒いクロップドパンツ、ストラクチャードなシルエットでモード感を強調",
                    "inner": "黒いシルク製キャミソール  、通気性が良く軽量な素材",
                    "shoes": "ブラックのプラットフォームブーツ、モードスタイルをさらに引き立てるデザイン",
                    "accessory": "黒いアシンメトリックなデザインのイヤリング、モードスタイルに相応しい個性的なアクセント"
                    })
                },
                {
                    "role": "user",
                    "content": result
                }
            ]
        )
        print(completion.choices[0].message)
        data = json.loads(completion.choices[0].message["content"])
        print(data)
        prompt = "Desired {height}cm {weight}kg {gender} full body styling, image(Season: {season}, Scene: {situation},  Age: {age}s, style: {style}, favorite color: {color}, Tops: {tops}, Bottom: {bottoms}, Shoes: {shoes}, accessory:{accessory}, Favorite Brand: {brand})".format(height=height, weight=weight, gender={gender}, season={get_season()}, 
        situation={situation}, age={age}, brand={brand}, style={style}, color={color}, tops={data['tops']}, bottoms={data['bottoms']}, shoes={data['shoes']},accessory={data['accessory']})

        translator_prmpt = translate(prompt)

        #profile情報から身体に関しての情報を取得する    
        #   prompt = "Desired 170cm 45kg female full body styling, image(Season: Spring, Scene: party,  Age: 20s, style: minimal style, favorite color: black, Tops: oversize tailored jacket, Bottom: Flounce Detail Midi Skirt, Shoes: black ballet shoes, socks:flower-patterned socks, Favorite Brand: simone rocha)"
        response = openai.Image.create(
            prompt = translator_prmpt,
            n = 1,
            size="1024x1024"
        )
        #生成した画像は保存するようにする
        return Response(response['data'], status=status.HTTP_200_OK)