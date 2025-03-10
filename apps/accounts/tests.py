from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from apps.accounts.models import UserProfile


class AccountsTests(TestCase):
    def setUp(self):
        """Create a test user"""
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_user_profile_created(self):
        """Check if the user profile is created automatically"""
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())

    def test_login(self):
        """Testing logging in"""
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "testpass"}
        )
        self.assertRedirects(
            response, "/refunds/"
        )  # After login, redirect to the list of refunds

    def test_logout(self):
        """Testing logging out"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("logout"))
        self.assertRedirects(
            response, reverse("login")
        )  # After exit redirect to the login page

    def test_signup(self):
        """Testing new user registration"""
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "newuser@exapmle.com",
                "password1": "TestPass123!",
                "password2": "TestPass123!",
            },
        )
        self.assertRedirects(
            response, reverse("login")
        )  # After registration redirect to login
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_password_reset(self):
        """Testing password reset"""
        response = self.client.post(
            reverse("password_reset"), {"email": self.user.email}
        )
        self.assertEqual(response.status_code, 200)
