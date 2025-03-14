from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.models import Note
from notes.tests.test_class import TestAuthorNoteUrl
#from notes.tests.core.class_in_test import TestAuthorNoteUrl
User = get_user_model()


class TestRoutes(TestAuthorNoteUrl):

    '''@classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Lena')
        cls.reader = User.objects.create(username='Читатель')
        cls.notes = Note.objects.create(
            author=cls.author,
            text='Текст комментария',
            title='Заголовок',
            slug='Slug')'''

    def test_pages_availability(self):
        # Доступ к страницам логина,главной и отдельной страницы
        self.client.force_login(self.author)
        urls = (
            ('notes:home', None),
            ('notes:detail', (self.note.slug,)),
            ('notes:add', None),
            ('notes:list', None),
            ('notes:success', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_comment_edit_and_delete(self):
        # Проверка доступности страниц удаления и редактирования
        users_statuses = ((self.author, HTTPStatus.OK),
                          (self.no_author, HTTPStatus.NOT_FOUND),)
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:edit', 'notes:delete'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        # Проверка редиректа для страниц удалени и редактирования
        login_url = reverse('users:login')
        for name in ('notes:edit', 'notes:delete'):
            with self.subTest(name=name):
                url = reverse(name, args=(self.note.slug,))
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
