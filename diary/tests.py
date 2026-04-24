from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Entry


class EntryPermissionTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(
            username="owner",
            password="testpass123",
        )
        self.other_user = user_model.objects.create_user(
            username="other",
            password="testpass123",
        )
        self.entry = Entry.objects.create(
            user=self.owner,
            title="最初の日記",
            content="本文です。",
        )

    def test_create_requires_login(self):
        response = self.client.get(reverse("diary:entry_create"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('diary:entry_create')}",
        )

    def test_login_page_is_available(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)

    def test_non_owner_cannot_update_entry(self):
        self.client.login(username="other", password="testpass123")

        response = self.client.post(
            reverse("diary:entry_update", args=[self.entry.pk]),
            {"title": "書き換え", "content": "変更された本文"},
            follow=True,
        )

        self.entry.refresh_from_db()
        self.assertRedirects(response, reverse("diary:entry_list"))
        self.assertEqual(self.entry.title, "最初の日記")

    def test_non_owner_cannot_delete_entry(self):
        self.client.login(username="other", password="testpass123")

        response = self.client.post(
            reverse("diary:entry_delete", args=[self.entry.pk]),
            follow=True,
        )

        self.assertRedirects(response, reverse("diary:entry_list"))
        self.assertTrue(Entry.objects.filter(pk=self.entry.pk).exists())


class SignUpTests(TestCase):
    def test_signup_page_is_available(self):
        response = self.client.get(reverse("diary:signup"))

        self.assertEqual(response.status_code, 200)

    def test_user_can_signup(self):
        response = self.client.post(
            reverse("diary:signup"),
            {
                "username": "newuser",
                "password1": "strong-pass-123",
                "password2": "strong-pass-123",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("diary:entry_list"))
        self.assertTrue(get_user_model().objects.filter(username="newuser").exists())
        self.assertEqual(str(response.context["user"]), "newuser")
