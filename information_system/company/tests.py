from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Person
from.serializers import PersonSerializer


class PersonApiTestCase(APITestCase):
    def setUp(self):
        self.person = Person.objects.create(first_name='Taras', second_name='Khab', middle_name='Myros', passport='PP908070',
                                       birthday='1988-02-27', place_birthday='Lviv', address='Shevchenka street')
        self.person.save()

    def test_get(self):
        response = self.client.get('/api/v1/persons/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0], PersonSerializer(self.person).data)

    def test_post(self):
        response = self.client.post('/api/v1/persons/', headers={'auth-token': 'string'})


    def tearDown(self):
        self.person.delete()
