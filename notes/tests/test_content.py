from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note
from notes.tests.test_class import TestAuthorNoteUrl

User = get_user_model()


class TestHomePage(TestAuthorNoteUrl):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Lena')
        cls.no_author = User.objects.create(username='Gena')
        cls.note = Note.objects.create(
            author=cls.author,
            text='Текст комментария',
            title='Заголовок',
            slug='Slug')
        cls.list_url = reverse('notes:list')
        cls.add_url = reverse('notes:add')
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))

    def test_note_in_list(self):
        # Проверка заметка отображается в списке заметок
        self.client.force_login(self.author)
        response = self.client.get(self.list_url)
        self.assertIn(self.note, response.context['object_list'])

    def test_no_list_for_no_author(self):
        # Не автор доступа к листу заметок не имеет
        self.client.force_login(self.no_author)
        response = self.client.get(self.list_url)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_form_in_add_and_edit(self):

        # Проверка передачи формы на страницы редактирования и создания
        urls_form = ((self.edit_url, 'form'), (self.add_url, 'form'))
        self.client.force_login(self.author)
        for url, form in urls_form:
            with self.subTest (url=url, form=form):
                response = self.client.get(url)
                self.assertIn(form, response.context)
