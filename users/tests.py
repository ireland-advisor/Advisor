from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.utils import json

from users.models import Profile
from users.serializers import ProfileSerializer


class UserTest(TestCase):
    def create_user(self, user_name='lee', user_email='lee197@gmail.com'):
        return User.objects.create(email=user_email, username=user_name)

    # models
    def test_create_user(self):
        user = self.create_user()
        self.assertTrue(isinstance(user, User))

    # views
    def test_uers_list_view(self):
        url = reverse('user-list')
        user = self.create_user()
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(user.username.encode(), resp.content)

    def test_uers_detail_view(self):
        url = reverse('user-detail', args=(1,))
        user = self.create_user()
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(user.username.encode(), resp.content)


class GroupTest(TestCase):
    def create_group(self, group_name='advisor'):
        return Group.objects.create(name=group_name)

    # models
    def test_create_group(self):
        group = self.create_group()
        self.assertTrue(isinstance(group, Group))

    # views
    def test_group_list_view(self):
        url = reverse('group-list')
        group = self.create_group()
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(group.name.encode(), resp.content)

    def test_group_detail_view(self):
        url = reverse('group-detail', args=(1,))
        group = self.create_group()
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(group.name.encode(), resp.content)


# api
class MentorTest(APITestCase):
    def setUp(self) -> None:
        self.mentor_list_url = reverse("mentors-list")
        self.mentor_detail_url = reverse("mentors-detail", args=(1,))

        self.GENDER_CHOICES = (("0", "male"), ("1", "female"))

        self.mentor_first_name = "lee"
        self.mentor_middle_name = "qi"
        self.mentor_last_name = "la"
        self.mentor_gender = self.GENDER_CHOICES[0][0]
        self.mentor_title = 'CEO'
        self.mentor_des = 'he is genious'
        self.mentor_expert = 'coding'

        self.mentor = Profile.objects.create(first_name=self.mentor_first_name,
                                             middle_name=self.mentor_middle_name,
                                             last_name=self.mentor_last_name,
                                             gender=self.mentor_gender,
                                             title=self.mentor_title,
                                             expertiseFields=self.mentor_expert,
                                             des=self.mentor_des)

        self.mentor.save()

    def tearDown(self) -> None:
        self.mentor.delete()

    def test_post_mentor_list(self):
        mentor_serializer_data = json.dumps(ProfileSerializer(instance=self.mentor).data)
        resp = self.client.post(self.mentor_list_url, mentor_serializer_data, content_type='application/json')
        self.assertEqual(201, resp.status_code)
        self.assertIn(self.mentor.title.encode(), resp.content)

    def test_get_mentor_list(self):
        resp = self.client.get(self.mentor_list_url)
        self.assertEqual(200, resp.status_code)
        self.assertIn(self.mentor.title.encode(), resp.content)

    def test_put_mentor_detail(self):
        mentor_serializer_data = json.dumps(ProfileSerializer(instance=self.mentor).data)
        resp = self.client.put(self.mentor_detail_url, mentor_serializer_data, content_type='application/json')
        self.assertEqual(200, resp.status_code)
        self.assertIn(self.mentor.title.encode(), resp.content)

    def test_get_mentor_detail(self):
        resp = self.client.get(self.mentor_detail_url, content_type='application/json')
        self.assertEqual(200, resp.status_code)
        self.assertIn(self.mentor.title.encode(), resp.content)