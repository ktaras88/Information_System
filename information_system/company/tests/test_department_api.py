from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import Department, Employee, Person, Position
from ..serializers import DepartmentSerializer


class DepartmentApiTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', email='email@em.com', password='good-password')
        refresh = RefreshToken.for_user(user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.person1 = Person.objects.create(first_name='Name1', second_name='N1', middle_name='NN1',
                        passport='PP908070', birthday='1988-02-27', place_birthday='Lviv', address='Some1 street')
        self.person2 = Person.objects.create(first_name='Name2', second_name='N2', middle_name='NN2',
                        passport='PP908070', birthday='1988-02-27', place_birthday='Lviv', address='Some2 street')
        self.position1 = Position.objects.create(position='Junior', rate=1000, vacation_days=20)
        self.employee1 = Employee.objects.create(person_id=self.person1, position_id=self.position1,
                                                 employment_date='2022-01-01', fired_date='2023-01-01')
        self.employee2 = Employee.objects.create(person_id=self.person2, position_id=self.position1,
                                                 employment_date='2022-02-02', fired_date='2023-02-02')
        self.dep1 = Department.objects.create(name='Dep1', abbreviation='D1')
        self.dep2 = Department.objects.create(name='Dep2', abbreviation='D2')
        self.data = {
            'name': 'Department',
            'abbreviation': 'DEP',
            'max_amount': 20,
            'employees': [self.employee1.id, self.employee2.id]
        }

    def tearDown(self):
        del self.person1, self.person2
        del self.position1
        del self.employee1, self.employee2
        del self.dep1, self.dep2
        del self.data

    def test_get(self):
        response = self.client.get('/api/v1/departments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, DepartmentSerializer((self.dep1, self.dep2), many=True).data)

    def test_post_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post('/api/v1/departments/', self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_authenticated(self):
        response = self.client.post('/api/v1/departments/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Department')

    def test_post_authenticated_bad_request(self):
        data = {
            'name': 'Department',
            'abbreviation': 'DEP',
            'max_amount': 20,
            # 'employees': [self.employee1.id, self.employee2.id]
        }
        response = self.client.post('/api/v1/departments/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_limit_employees_in_department(self):
        employees21 = []
        for i in range(21):
            employee0 = Employee.objects.create(person_id=self.person1, position_id=self.position1,
                                                employment_date='2022-01-01', fired_date='2023-01-01')
            employees21.append(employee0.id)
        id_dep1 = self.dep1.id
        response = self.client.put(f'/api/v1/departments/{id_dep1}/', {
                'name': 'Department',
                'abbreviation': 'DEP',
                'max_amount': 20,
                'employees': employees21
        })
        # self.assertEqual(response.status_code, 200)
        # ?????????????????????????

    def test_put_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        id_dep1 = self.dep1.id
        response = self.client.put(f'/api/v1/departments/{id_dep1}/', self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_authenticated(self):
        id_dep1 = self.dep1.id
        response = self.client.put(f'/api/v1/departments/{id_dep1}/', self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_authenticated(self):
        id_dep1 = self.dep1.id
        response = self.client.delete(f'/api/v1/departments/{id_dep1}/', {'id': id_dep1})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Department.objects.all().count(), 1)

    def test_delete_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        id_dep1 = self.dep1.id
        response = self.client.delete(f'/api/v1/departments/{id_dep1}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class QuantityLimit(Exception):
    pass