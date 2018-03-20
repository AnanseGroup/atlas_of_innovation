from django.test import TestCase
from application.models.spaces import Space
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json

class SpaceTestCase(TestCase):

    fixtures = ['initial_database']

    def test_fixture_loading(self):
        """testing that the test fixtures load appropriately"""
        my_space = Space.objects.get(id=1)
        self.assertEqual(my_space.name, '42')

    def test_get_space(self):
        """The get_space API endpoint works"""
        url = reverse('get_space', kwargs={'id':1})
        response = self.client.get(url)
        space_dict = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(space_dict['name'], '42')