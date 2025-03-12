from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note


User = get_user_model()


class TestAuthorNoteUrl(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        cls.author = User.objects.create(username='Lena')
        cls.no_author = User.objects.create(username='Gena')
        cls.note = Note.objects.create(
            author=cls.author,
            text='Текст комментария',
            title='Заголовок',
            slug='Slug')
        '''cls.form_data = {'text': cls.NOTE_TEXT, 'title': cls.NOTE_TITLE,
                         'author': cls.auth_client, }'''
        cls.list_url = reverse('notes:list')
        cls.add_url = reverse('notes:add')
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
