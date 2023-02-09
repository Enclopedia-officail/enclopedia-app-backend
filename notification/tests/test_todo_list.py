from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from notification.models import Todo

TODO_LIST_URL = reverse('notification:todo_list')

class TodoModeTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            first_name = 'test',
            last_name = 'test',
            username = 'test',
            email = 'test@example.com',
            phone_number = '09001610001',
            password = 'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_crate_todo(self):
        todo = Todo.objects.create(
            user = self.user,
            title = 'test',
            thumbnail = 'https://api.test.com',
            url = 'https://api.example.com'
        )

        self.assertEqual(todo.title, 'test')

class TodoListTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            first_name = 'test',
            last_name = 'test',
            username = 'test',
            email = 'test@example.com',
            phone_number = '09001610001',
            password = 'testpass123',
        )
        self.client.force_authenticate(self.user)
    
    def test_todo_list(self):
        for n in range(3):
            Todo.objects.create(
                user = self.user,
                title = 'test{}'.format(n),
                thumbnail = 'https://api.test{}.com'.format(n),
                url = 'https://api.example{}.com'.format(n)
            )
        res = self.client.get(TODO_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

class TodoUpdateTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            first_name = 'test',
            last_name = 'test',
            username = 'test',
            email = 'test@example.com',
            phone_number = '09001610001',
            password = 'testpass123',
        )
        self.client.force_authenticate(self.user)

        self.todo = Todo.objects.create(
            user = self.user,
            title = 'test',
            thumbnail = 'https://api.testcom',
            url = 'https://api.exampl.com'
        )
    
    def test_todo_update(self):
        url = 'https://api.enclopedia-official.com/api/notification/todo/{}'.format(self.todo.id)
        res = self.client.patch(url, data={'todo': True})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['todo'], True)