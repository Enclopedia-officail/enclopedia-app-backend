from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import generics
from rest_framework import status
from .models import News, Notification, Read, Todo
from .serializers import ListReadSerialzier, NewsSerializer, NewsListSerialzier, NotificationListSerializer, NotificationSerializer, TodoSerializer

#administrator側のみで作成
class NewsCreateView(generics.CreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = News.objects.all()
    serializer_class = NewsSerializer

#Newswos
class NewsView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = News.objects.order_by('-created_at').all()
    serializer_class = NewsSerializer
    lookup_fields = 'pk'

class NotificationRetreiveView(generics.RetrieveAPIView):
    queryset = Notification.objects.order_by('-created_at').all()
    serializer_class = NotificationSerializer
    lookup_fields = 'pk'

class NotificationView(generics.CreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Notification.objects.order_by('-created_at').all()
    serializer_class = NotificationSerializer


#未読の数のみを返すtable
class ReadListView(generics.ListAPIView):
    queryset = Read.objects.select_related('account').all()
    serializer_class = ListReadSerialzier

    def get(self, request):
        user = request.user
        activities = get_list_or_404(self.queryset, account=user, read=False)
        return Response(len(activities), status=status.HTTP_200_OK)

#上の処理と共に記述する
#未読状態から既読状態にする
class AlreadyReadView(APIView):
    serializer_class = ListReadSerialzier
    queryset = Read.objects.all()

    def put(self, request, *args, **kwargs):
        user = request.user
        reads = get_list_or_404(self.queryset, account=user, read=False)
        read_list = []
        for read in reads:
            read.read = True
            read_list.append(read)
        Read.objects.bulk_update(read_list, fields=['read'])
        return Response(0, status=status.HTTP_200_OK)


#ニュースを一覧取得する
class NewsListView(generics.ListAPIView):
    
    serializer_class = NewsListSerialzier
    queryset = News.objects.order_by('-created_at').defer('body', 'url').all()
    permission_classes = (AllowAny,)
    def get(self, request):
        news = get_list_or_404(self.queryset)
        serializer = self.serializer_class(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#userへ穂通知を取得する
class NotificationListView(generics.ListAPIView):
    serializer_class =NotificationListSerializer
    queryset = Notification.objects.order_by('-created_at').defer('body', 'url').all()

    def get(self, request):
        user = request.user
        notifications = get_list_or_404(self.queryset, user=user)
        serializer = self.serializer_class(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#完了していないやることリストを一覧で取得する
class TodoListView(generics.ListAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.order_by('-created_at').select_related('user').all()
    def get(self, request):
        user = request.user
        todo = get_list_or_404(self.queryset, user=user, todo=False)
        serializer = self.serializer_class(todo, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TodoCompletedView(generics.UpdateAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.order_by('-created_at').select_related('user').all()
    def put(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(self.queryset, id=pk)
        instance.todo = request.data['todo']
        instance.save()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)