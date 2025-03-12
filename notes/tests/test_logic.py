from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestAddEditDeleteNote(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор настоящий')
        cls.note = Note.objects.create(
            author=cls.author,
            text='Текст комментария',
            title='Заголовок',
            slug='Slug')
        cls.add_url = reverse('notes:add')
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.done_url = reverse('notes:success')
        cls.user = User.objects.create(username='Не авторизованный юзер')
        cls.user = Client()
        cls.author_client = Client()
        # "Логиним" пользователя в клиенте.
        cls.author_client.force_login(cls.author)
        # Делаем всё то же самое для пользователя-читателя.
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

    def test_add_note_user_no_login(self):
        # Анонимный пользователь не может создать заметку
        response = self.user.post(self.add_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_add_note_author_login(self):
        # Добавление заметки авторизованным пользователем
        response = self.author_client.post(self.add_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_autor_or_reader(self):
        # Доступ на страницу редактирования для автора и читателя
        user_status = ((self.author_client, HTTPStatus.OK),
                       (self.reader_client, HTTPStatus.NOT_FOUND))
        for user, status in user_status:
            response = user.post(self.edit_url)
            self.assertEqual(response.status_code, status)

    def test_delete_author(self):
        # Автор может удалить свою заметку
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.done_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_delete_reader(self):
        # Не автор не может удалить заметку
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)


class TestAddNoteNoSlug(TestCase):
    NOTE_TEXT = 'Текст заметки'
    NOTE_TITLE = 'Текст заголовка'
    NOTE_SLUG = 'slug'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Лента')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {'text': cls.NOTE_TEXT, 'title': cls.NOTE_TITLE,
                         'author': cls.auth_client, }

    def test_add_note_no_slug(self):
        # Параметр слуг можно не указывать, он будет присвоен title
        response = self.auth_client.post(reverse('notes:add'),
                                         data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)


class TestNoteSlugDublicat(TestCase):
    # Нельзя создать запись с уже существующим slug
    def test_slug(self):
        add_url = reverse('notes:add')
        author = User.objects.create(username='Автор настоящий')
        author_client = Client()
        author_client.force_login(author)
        note = Note.objects.create(
            author=author,
            text='Текст комментария из четвертого класса',
            title='Заголовок', slug='New')
        note_obj = Note.objects.get()
        print(note_obj.slug)
        print(note.slug == note_obj.slug)
        notes_count = Note.objects.count()
        self.assertEqual(note_obj.slug, note.slug)
        author_client.post(add_url, data={
            'title': 'Заголовок', 'text': 'текст', 'slug': 'New'})
        '''self.assertFormError(response, 'form', 'slug',
                             errors=(self.note.slug + WARNING))'''
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
