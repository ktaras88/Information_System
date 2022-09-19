from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import Position
from ..serializers import PositionSerializer


class PositionApiTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', email='email@em.com', password='good-password')
        refresh = RefreshToken.for_user(user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.position1 = Position.objects.create(position='Jun', rate=1000, vacation_days=20)
        self.position2 = Position.objects.create(position='Mid', rate=2000, vacation_days=25)
        self.data = {
            "position": "Sen",
            "rate": 3000,
            "vacation_days": 30
        }

    def tearDown(self):
        del self.position1, self.position2
        del self.data

    def test_get(self):
        response = self.client.get('/api/v1/positions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, PositionSerializer((self.position1, self.position2), many=True).data)

    def test_post_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post('/api/v1/positions/', self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_authenticated(self):
        response = self.client.post('/api/v1/positions/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['position'], 'Sen')

    def test_post_authenticated_bad_request(self):
        data = {
            "position": "Sen",
            "rate": 3000,
            # "vacation_days": 30
        }
        response = self.client.post('/api/v1/positions/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        id_position1 = self.position1.id
        response = self.client.put(f'/api/v1/positions/{id_position1}/', self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_un_authenticated(self):
        id_position1 = self.position1.id
        response = self.client.put(f'/api/v1/positions/{id_position1}/', self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_authenticated(self):
        id_position1 = self.position1.id
        response = self.client.delete(f'/api/v1/positions/{id_position1}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Position.objects.all().count(), 1)

    def test_delete_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        id_position1 = self.position1.id
        response = self.client.delete(f'/api/v1/positions/{id_position1}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
