from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import Employee, Position, Person
from ..serializers import EmployeeSerializer


class EmployeeApiTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', email='email@em.com', password='good-password')
        refresh = RefreshToken.for_user(user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.person1 = Person.objects.create(first_name='Name1', second_name='N1', middle_name='NN1',
                        passport='PP908070', birthday='1988-02-27', place_birthday='Lviv', address='Shevchenka street')
        self.person2 = Person.objects.create(first_name='Name2', second_name='N2', middle_name='NN2',
                        passport='PP908070', birthday='1988-02-27', place_birthday='Lviv', address='Shevchenka street')
        self.position1 = Position.objects.create(position='Jun', rate=1000, vacation_days=20)
        self.position2 = Position.objects.create(position='Mid', rate=2000, vacation_days=25)
        self.employee1 = Employee.objects.create(person_id=self.person1, position_id=self.position1,
                                                 employment_date='2020-10-01', fired_date='2022-10-01')
        self.employee2 = Employee.objects.create(person_id=self.person2, position_id=self.position2,
                                                 employment_date='2020-10-01', fired_date='2022-10-01')
        self.data = {
            'person_id': self.person2.id,
            'position_id': self.position2.id,
            'employment_date': '2000-01-01',
            'fired_date': '2022-01-01'
        }

    def tearDown(self):
        del self.person1, self.person2
        del self.position1, self.position2
        del self.employee1, self.employee2
        del self.data

    def test_get(self):
        response = self.client.get('/api/v1/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, EmployeeSerializer((self.employee1, self.employee2), many=True).data)

    def test_post_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post('/api/v1/employees/', self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_un_authenticated(self):
        response = self.client.post('/api/v1/employees/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['employment_date'], '2000-01-01')

    def test_post_authenticated_bad_request(self):
        data = {
            # 'person_id': self.person2.id,
            'position_id': self.position2.id,
            'employment_date': '2000-01-01',
            'fired_date': '2022-01-01'
        }
        response = self.client.post('/api/v1/employees/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        id_employee1 = self.employee1.id
        response = self.client.put(f'/api/v1/employees/{id_employee1}/', self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_un_authenticated(self):
        id_employee1 = self.employee1.id
        response = self.client.put(f'/api/v1/employees/{id_employee1}/', self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_authenticated(self):
        id_employee1 = self.employee1.id
        response = self.client.delete(f'/api/v1/employees/{id_employee1}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.all().count(), 1)

    def test_delete_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        id_employee1 = self.employee1.id
        response = self.client.delete(f'/api/v1/employees/{id_employee1}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
