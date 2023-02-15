from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Read, News, Notification, Todo

#ポリモーフィック獲得時にはtitleとidのみ必要
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id','title', 'body', 'url', 'created_at']

#作成した際には自動的にpush通知,メール通知とActivitietableの作成を行うようにする
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'body', 'url', 'created_at']

#listの場合
class NewsListSerialzier(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'created_at']

class NotificationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'created_at']

#read
class ReadSerializer(serializers.RelatedField):
    #serializernewsornotificationのインスタスを作成するようにする
    def to_representation(self, value):
        if isinstance(value, News):
            serializer = NewsSerializer(value)
        elif isinstance(value, Notification):
            serializer = NotificationSerializer(value, Notification)
        else:
            raise Exception('予期せぬエラーが発生しました。')
        return serializer.data

#titleと一緒に返す必要がある
class ListReadSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Read
        fields = ['id', 'read', 'content_type', 'object_id']

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'created_at', 'url', 'todo', 'content_type', 'object_id']

