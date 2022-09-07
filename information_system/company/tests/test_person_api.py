from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import Person
from ..serializers import PersonSerializer


class PersonApiTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', email='email@em.com', password='good-password')
        refresh = RefreshToken.for_user(user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.person1 = Person.objects.create(first_name='Name1', second_name='N1', middle_name='NN1',
                        passport='PP908070', birthday='1988-02-27', place_birthday='Lviv', address='Shevchenka street')
        self.person2 = Person.objects.create(first_name='Name2', second_name='N2', middle_name='NN2',
                        passport='PP908070', birthday='1988-02-27', place_birthday='Lviv', address='Shevchenka street')
        self.person1.save()
        self.person2.save()
        self.data = {
            "first_name": "Name",
            "second_name": "Second_name",
            "middle_name": "Middle_name",
            "passport": "KL908070",
            "birthday": "1988-02-27",
            "place_birthday": "Lviv",
            "address": "Shevchenka street"
        }

    def test_get(self):
        response = self.client.get('/api/v1/persons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, PersonSerializer((self.person1, self.person2), many=True).data)

    def test_post_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post('/api/v1/persons/', self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_authenticated(self):
        response = self.client.post('/api/v1/persons/', self.data)  # headers={'auth-token': 'string'}
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'Name')

    def test_post_authenticated_bad_request(self):
        data = {
            "second_name": "Second_name",
            "middle_name": "Middle_name",
            "passport": "KL908070",
            "birthday": "1988-02-27",
            "place_birthday": "Lviv",
            "address": "Shevchenka street"
        }
        response = self.client.post('/api/v1/persons/', data)  # headers={'auth-token': 'string'}
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.put('/api/v1/persons/1/', self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_authenticated(self):
        Person.objects.create(
            id=1,
            first_name='N1',
            second_name='N11',
            middle_name='N111',
            passport='PP908070',
            birthday='1988-12-27',
            place_birthday='Lviv',
            address='Shevchenka street')

        response = self.client.put('/api/v1/persons/1/', self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        pass
