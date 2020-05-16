from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import MentoringTags, SeekingTags, Profile
from profiles.serializers import ProfileSerializer, ProfileDetailSerializer

PROFILES_URL = reverse('profile:profile-list')


def sample_mentor_tag(user, name='mentor'):
    """Create and return a sample mentor tag"""
    return MentoringTags.objects.create(user=user, name=name)


def sample_seeker_tag(user, name='seeker'):
    """Create and return a sample seeker tag"""
    return SeekingTags.objects.create(user=user, name=name)


def detail_url(profile_id):
    """Return profile detail URL"""
    return reverse('profile:profile-detail', args=[profile_id])


def sample_profile(user, **params):
    """Create and return a sample profile"""
    defaults = {
        'title': 'lee',
        'personal_des': 'this is me who is working hard',
        'birthday': '1990-10-19',
    }
    defaults.update(params)

    return Profile.objects.create(user=user, **defaults)


class PublicProfilesApiTests(TestCase):
    """Test unauthenticated profile API access"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test the authenticaiton is required"""
        res = self.client.get(PROFILES_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateProfileApiTests(TestCase):
    """Test authenticated profile API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            first_name='testpass',
            last_name='testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_profiles(self):
        """Test retrieving list of profiles"""
        sample_profile(user=self.user)
        sample_profile(user=self.user)

        res = self.client.get(PROFILES_URL)

        profiles = Profile.objects.all().order_by('-id')
        serializer = ProfileSerializer(profiles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 2)
        self.assertIn(res.data["results"][0], serializer.data)
        self.assertIn(res.data["results"][1], serializer.data)


    def test_view_profile_detail(self):
        """Test viewing a profile detail"""
        profile = sample_profile(user=self.user)
        profile.seeking_tags.add(sample_seeker_tag(user=self.user))
        profile.mentoring_tags.add(sample_mentor_tag(user=self.user))

        url = detail_url(profile.id)
        res = self.client.get(url)

        serializer = ProfileDetailSerializer(profile)
        self.assertEqual(res.data, serializer.data)

    def test_create_profile_with_tags(self):
        """Test creating a profile with tags"""
        mentor_tag1 = sample_mentor_tag(user=self.user, name='Mentor Tag 1')
        mentor_tag2 = sample_mentor_tag(user=self.user, name='Mentor Tag 2')

        seeker_tag1 = sample_seeker_tag(user=self.user, name='Seeker Tag 1')
        seeker_tag2 = sample_seeker_tag(user=self.user, name='Seeker Tag 2')

        payload = {
            'title': 'Test profile with two tags',
            'mentoring_tags': [mentor_tag1.id, mentor_tag2.id],
            'seeking_tags': [seeker_tag1.id, seeker_tag2.id],
            'birthday': '1993-10-10',
            'personal_des': 'I will never give up'
        }
        res = self.client.post(PROFILES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        profile = Profile.objects.get(id=res.data['id'])
        mentor_tags = profile.mentoring_tags.all()
        seeker_tags = profile.seeking_tags.all()

        self.assertEqual(mentor_tags.count(), 2)
        self.assertIn(mentor_tag1, mentor_tags)
        self.assertIn(seeker_tag1, seeker_tags)

    def test_partial_update_profile(self):
        """Test updating a profile with patch"""
        profile = sample_profile(user=self.user)
        profile.mentoring_tags.add(sample_mentor_tag(user=self.user))
        new_tag = sample_mentor_tag(user=self.user, name='curry')

        payload = {'title': 'lee', 'mentoring_tags': [new_tag.id]}
        url = detail_url(profile.id)
        self.client.patch(url, payload)

        profile.refresh_from_db()
        self.assertEqual(profile.title, payload['title'])
        tags = profile.mentoring_tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)
