import json

from django.test import TestCase
from django.urls import reverse

from .models import User


class JWTLoginTests(TestCase):
    def test_login_with_email_and_password_sets_http_only_cookies(self):
        user = User.objects.create_user(
            email='admin@example.com',
            password='senha123',
            first_name='Admin',
            last_name='User',
        )

        response = self.client.post(
            reverse('token_obtain_pair'),
            data=json.dumps({'email': user.email, 'password': 'senha123'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Login bem-sucedido"})
        self.assertIn('access', response.cookies)
        self.assertIn('refresh', response.cookies)
        self.assertTrue(response.cookies['access']['httponly'])
        self.assertTrue(response.cookies['refresh']['httponly'])
        self.assertTrue(response.cookies['access'].value)
        self.assertTrue(response.cookies['refresh'].value)
