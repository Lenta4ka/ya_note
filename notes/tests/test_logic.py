from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

# Импортируем из файла с формами список стоп-слов и предупреждение формы.
# Загляните в news/forms.py, разберитесь с их назначением.

from notes.models import Note

User = get_user_model()


class TestAddEditDeleteNote(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор настоящий')
        cls.note = Note.objects.create( author=cls.author,
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
        response = self.user.post(self.add_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
    
    def test_add_note_author_login(self):
        response = self.author_client.post(self.add_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_autor_or_reader(self):
        user_status = ((self.author_client, HTTPStatus.OK),(self.reader_client, HTTPStatus.NOT_FOUND))
        for user, status in user_status:

            response = user.post(self.edit_url)
            self.assertEqual(response.status_code, status)

    def test_delete_author(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.done_url )
        notes_count = Note.objects.count()
        # Ожидаем ноль комментариев в системе.
        self.assertEqual(notes_count, 0) 

    def test_delete_reader(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1) 
 
class TestAddNoteNoSlug(TestCase):

    def test_add_note_no_slug(self):
        author = User.objects.create(username='Автор настоящий')
        note = Note.objects.create(author=author,
            text='Текст комментария из второго класса',
            title='Заголовок из второго класса',)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1) 

class TestNoteSlugDublicat(TestCase):
    def test_slug(self):
        add_url = reverse('notes:add')
        author = User.objects.create(username='Автор настоящий')
        author_client = Client()
        # "Логиним" пользователя в клиенте.
        author_client.force_login(author)
        note = Note.objects.create(author=author,
            text='Текст комментария из четвертого класса',
            title='Заголовок',slug='New')
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        response = author_client.post(add_url, data = {
            'title':'Заголовок','text':'текст','slug':'New'})
        #self.assertFormError(response,'form', 'slug',)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)