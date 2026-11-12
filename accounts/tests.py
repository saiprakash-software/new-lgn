
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class LoginSignupTests(TestCase):

    def setUp(self):
        # Create one test user before every test
        self.email = "test@example.com"
        self.password = "Test@12345"

        self.user = User.objects.create_user(
            username=self.email,
            email=self.email,
            password=self.password
        )

        self.login_url = reverse("login")
        self.dashboard_url = reverse("dashboard")

    # 1. Login page test
    def test_login_page_loads(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)

    # 2. Correct password test
    def test_correct_password_login(self):
        response = self.client.post(
            self.login_url,
            {
                "action": "login",
                "email": self.email,
                "password": self.password
            }
        )

        self.assertRedirects(response, self.dashboard_url)

    # 3. Wrong password test
    def test_wrong_password_rejected(self):
        response = self.client.post(
            self.login_url,
            {
                "action": "login",
                "email": self.email,
                "password": "WrongPassword123"
            },
            follow=True
        )

        self.assertContains(
            response,
            "Incorrect password. Please try again."
        )

    # 4. Unknown email test
    def test_unknown_email_rejected(self):
        response = self.client.post(
            self.login_url,
            {
                "action": "login",
                "email": "unknown@example.com",
                "password": "Test@12345"
            },
            follow=True
        )

        self.assertContains(
            response,
            "Please create an account first."
        )

    # 5. Signup test
    def test_successful_signup(self):
        response = self.client.post(
            self.login_url,
            {
                "action": "signup",
                "name": "New User",
                "email": "new@example.com",
                "password": "NewUser123",
                "terms": "on"
            },
            follow=True
        )

        self.assertTrue(
            User.objects.filter(email="new@example.com").exists()
        )

        self.assertContains(
            response,
            "Registration successful."
        )

    # 6. Duplicate email test
    def test_duplicate_email_rejected(self):
        response = self.client.post(
            self.login_url,
            {
                "action": "signup",
                "name": "Another User",
                "email": self.email,
                "password": "NewUser123",
                "terms": "on"
            },
            follow=True
        )

        self.assertContains(
            response,
            "Email already registered. Please login."
        )

        self.assertEqual(
            User.objects.filter(email=self.email).count(),
            1
        )

    # 7. Dashboard protection test
    def test_dashboard_requires_login(self):
        response = self.client.get(self.dashboard_url)

        self.assertRedirects(response, self.login_url)
