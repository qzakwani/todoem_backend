from django.test import TestCase
from django.core import validators
from django.core.exceptions import ValidationError
from .models import User

class UserModelTest(TestCase):
    
    def test_username_field(self):
        user = User(username='testuser')
        user.full_clean()
        user.save()
        self.assertEqual(user.username, 'testuser')
        
    def test_username_unique(self):
        User.objects.create(username='testuser')
        user = User(username='testuser')
        with self.assertRaises(ValidationError) as cm:
            user.full_clean()
            user.save()
        self.assertEqual(cm.exception.message_dict, {'username': ['A user with that username already exists.']})
        
    def test_password_field(self):
        user = User(password='password')
        with self.assertRaises(ValidationError) as cm:
            user.full_clean()
            user.save()
        self.assertEqual(cm.exception.message_dict, {'password': ['password length MUST be 6 characters or more']})
        
    def test_email_field(self):
        user = User(email='test@example.com')
        user.full_clean()
        user.save()
        self.assertEqual(user.email, 'test@example.com')
        
    def test_email_unique(self):
        User.objects.create(email='test@example.com')
        user = User(email='test@example.com')
        with self.assertRaises(ValidationError) as cm:
            user.full_clean()
            user.save()
        self.assertEqual(cm.exception.message_dict, {'email': ['User with this email already exists.']})
    
    def test_phone_number_field(self):
        user = User(phone_number='+1234567890')
        user.full_clean()
        user.save()
        self.assertEqual(user.phone_number, '+1234567890')
        
    def test_is_phone_number_verified_field(self):
        user = User(is_phone_number_verified=True)
        user.full_clean()
        user.save()
        self.assertTrue(user.is_phone_number_verified)
        
    def test_is_email_verified_field(self):
        user = User(is_email_verified=True)
        user.full_clean()
        user.save()
        self.assertTrue(user.is_email_verified)
        
    def test_private_field(self):
        user = User(private=True)
        user.full_clean()
        user.save()
        self.assertTrue(user.private)
        
    def test_display_name_property(self):
        user = User(username='testuser', name='Test User')
        user.full_clean()
        user.save()
        self.assertEqual(user.display_name, 'Test User')
        
    def test_str_method(self):
        user = User(username='testuser')
        user.full_clean()
        user.save()
        self.assertEqual(str(user), 'testuser')