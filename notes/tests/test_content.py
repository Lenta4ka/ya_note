# news/tests/test_content.py
from datetime import datetime, timedelta
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()
class TestHomePage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Lena')
        cls.notes = Note.objects.create( author=cls.author,
            text='Текст комментария',
            title='Заголовок',
            slug='Slug')
        cls.list_url = reverse('notes:list')
    def test_note_in_list(self):
        self.client.force_login(self.author)
        response = self.client.get(self.list_url)
        #print(self.notes in response.context['object_list'])
        # Проверяем, что сам объект новости находится в словаре контекста
        self.assertIn(self.notes, response.context['object_list'])
'''class TestHomePage(TestCase):

    HOME_URL = reverse('notes:home')
    
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Комментатор')
        today = datetime.today()
        cls.notes = Note.objects.create(
            author=cls.author,
            text='Текст комментария',
            title='Заголовок',
            slug='Slug')
        # Сохраняем в переменную адрес страницы с новостью:
        cls.list_url = reverse('notes:list')
        print(cls.list.url)
        #cls.author = User.objects.create(username='Комментатор')
all_notes = []
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
            notes = Note(title=f'Новость {index}', text='Просто текст.', date=today - timedelta(days=index))
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
                all_notes.append(notes)
        Note.objects.bulk_create(all_notes) 

    def test_note_in_list_notes(self):
        #self.client.force_login(self.author)
        #response = self.client.get(self.HOME_URL)
        #self.assertIn('notes', response.context)
        #print(response)
        # Проверяем, что объект новости находится в словаре контекста
        # под ожидаемым именем - названием модели.
        #self.assertIn('notes', response.context['notes_list'])
        # Загружаем главную страницу.
        response = self.client.get(self.list_url)
        self.assertIn('notes', response.context)
        # Код ответа не проверяем, его уже проверили в тестах маршрутов.
        # Получаем список объектов из словаря контекста.
        #object_list = response.context['object_list']
       # self.assertIn('note', response.context['object_list'])  
        # Определяем количество записей в списке.
        # Проверяем, что на странице именно 10 новостей.'''
        