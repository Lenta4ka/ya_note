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
        cls.no_author = User.objects.create(username='Gena')
        cls.note = Note.objects.create( author=cls.author,
            text='Текст комментария',
            title='Заголовок',
            slug='Slug')
        cls.list_url = reverse('notes:list')
        cls.add_url = reverse ('notes:add')
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        #cls.detail_url = reverse('notes:detail', args=(cls.note.slug,))

    def test_note_in_list(self):
        self.client.force_login(self.author)
        response = self.client.get(self.list_url)
        #print(self.note in response.context['object_list'])
        # Проверяем, что сам объект новости находится в словаре контекста
        self.assertIn(self.note, response.context['object_list'])

    def test_no_list_for_no_author(self):
        self.client.force_login(self.no_author)
        response = self.client.get(self.list_url)
        self.assertNotIn(self.note, response.context['object_list'])
        
    def test_form_in_add_and_edit(self):
        #self.add_url = reverse ('notes:add',args=(self.note.slug,))
        urls_form=((self.edit_url, 'form'),(self.add_url,'form'))
        self.client.force_login(self.author)
        for url, form in urls_form:

            response = self.client.get(url)
            self.assertIn(form, response.context)