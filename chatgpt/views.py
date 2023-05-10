from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files import File
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_list_or_404
from .models import Styling
from django.core.files.base import ContentFile
from urllib.request import urlopen
import environ
import datetime
import openai
import deepl
import json

from dateutil.relativedelta import relativedelta
from django.db.models import Q

env = environ.Env()
DEEPL_SECRET_KEY = env('DEEPL_SECRET_KEY')
CHATGPT_SECRET_API = env("CHATGPT_API_KEY")
openai.api_key = CHATGPT_SECRET_API


class StylingListView(generics.ListAPIView):
    queryset = Styling.objects.all()

    def get(self, request):
        start_of_month = datetime.datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_of_month = datetime.datetime.now().replace(day=1, hour=0, minute=0,second=0, microsecond=0) + relativedelta(months=1, days=0)
        object = get_list_or_404(self.queryset , user=request.user, created_at__gte=start_of_month, created_at__lte=end_of_month)
        data = {
            "number": len(object)
        }
        return Response(data, status=status.HTTP_200_OK)

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
    return result.text


class CreateImageView(APIView):
    #生成した画像からどのように洋服をおすすめするか?
    #生成できる画像に回数制限を設ける
    #生成に失敗した際のerrorハンドリングの修正
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
        tops_fit = data['tops_fit']
        bottoms_fit = data['bottoms_fit']
        bottoms_length = data['bottoms_length']
        season = get_season()

        #deepl
        content = "好きな色は{color}、服のシルエットは{silhouette}、好きなスタイルは{style}、好きなブランドは{brand}、服を着用するシーンは{situation}、好みの素材は{material}、身長は{height}cm、体重は{weight}kg、性別は{gender}、季節は{season}、トップスのシルエットは{tops_fit}、ボトムスのシルエットは{bottoms_fit}、ボトムスの丈は{bottoms_length}、尚アイテムに関しては情報をもとにtops(シャツ、ポロシャツ、ブラウス、カーディーガン、ニット、チュニック、ワンピース、ジャケット、コートなど）、\
                bottoms(デニム、スラックス、スカートなど）例に示したアイテムだけではなく考えられる全てのアイテムから情報に適したアイテムを選択すること。アイテムのカラーに関しては{color}を主体としつつ合うカラーパレットでスタイリングを組むこと。これらの情報をもとに{{tops:"", bottoms:"", inner:"",shoes:"",accessory:""}}ように前の返答と同様の形式でスタイリングを作成しデザインやディテールまで詳細にjson形式の文章のみで返して".format(
            color=color,silhouette=silhouette,style=style,brand=brand,situation=situation,material=material, height=height,weight=weight,gender=gender,season=season, tops_fit=tops_fit, bottoms_fit=bottoms_fit, bottoms_length=bottoms_length
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
                    "tops": "A black wool jacket with cutout detailing and an over-size silhouette. Perfect for parties and adding a punk edge to any outfit.",
                    "bottoms": "Long black wool trousers with a wide-leg silhouette and flowing movement. Perfect for pairing with the cutout over-size jacket for a complete YOHJI YAMAMOTO look.",
                    "inner": "COSのクルーネックニット。黒いボリュームのあるデザインで、ジャケットの内側に合わせます。",
                    "shoes": "Sleek and stylish black boots from Y-3, featuring a comfortable fit and modern design. Perfect for adding to a punk-inspired outfit.",
                    "accessory": "A black leather crossbody bag with studded detailing, perfect for adding an edgy element to any outfit. The perfect accessory for a punk-inspired party look."
                    })
                },
                {
                    "role": "user",
                    "content": result
                }
            ]
        )
        data = json.loads(completion.choices[0].message["content"])
        #promptにできればaccessory=data['accessory']の枠も加えるようにする
        prompt = "Full body styling of desired {gender} height {height} cm, weight {weight} kg, image( Season: {season}, Scene: {situation},  Age: {age}s, style: {style}, favorite color: {color}, Favorite Brand: {brand}, Tops: {tops}, Bottom: {bottoms}, Shoes: {shoes})".format(height=height, weight=weight, gender=gender, season=get_season(), 
        situation=situation, age=age, brand=brand, style=style, color=color, tops=data['tops'], bottoms=data['bottoms'], shoes=data['shoes'])

        translator_prmpt = translate(prompt)

        #profile情報から身体に関しての情報を取得する    
        #   prompt = "Desired 170cm 45kg female full body styling, image(Season: Spring, Scene: party,  Age: 20s, style: minimal style, favorite color: black, Tops: oversize tailored jacket, Bottom: Flounce Detail Midi Skirt, Shoes: black ballet shoes, socks:flower-patterned socks, Favorite Brand: simone rocha)"
        response = openai.Image.create(
            prompt = translator_prmpt,
            n = 1,
            size="1024x1024"
        )
        #画像をs3に保存しそのurlをurl fieldsに保存する処理を行
        url = urlopen(response['data'][0]['url'])
        chatgpt_image = url.read()
        print('start')
        print(chatgpt_image)
        file = ContentFile(chatgpt_image)
        Styling.objects.create(
            user=request.user, age=age, height=height, weight=weight, size=size, silhouette=silhouette,
            season=season, brand=brand, situation=situation, style=style, color=color, material=material, 
            tops_fit=tops_fit, bottoms_fit=bottoms_fit, bottoms_length=bottoms_length, image=file
        )
        #生成した画像は保存するようにする
        return Response(response['data'], status=status.HTTP_200_OK)