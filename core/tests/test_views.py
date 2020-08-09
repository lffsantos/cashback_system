import json
from unittest import TestCase

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Dealer


@pytest.mark.django_db(transaction=True)
class RestApiTest(TestCase):

    def setUp(self):
        data = {
            'email': "teste@gmail.com",
            'password': "123456"
        }
        self.dealer = Dealer.objects.create_dealer(name="teste", cpf="25020115070", **data)
        self.client = APIClient()
        url = reverse('obtain_token')

        response = self.client.post(url, data=data)
        self.token = response.data['token']

    # Cadastrp revendedor
    def test_create_dealer(self):
        url = reverse('core:dealer-list')
        data = {
            "email": "example@gmail.com",
            "name": 'Example',
            "cpf": "35767856044",
            "password": "123456",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Cadastro de compra
    def test_create_purchase_valid(self):
        url = reverse('core:purchase-list')
        auth = f'JWT {self.token}'
        data = {
            "purchase_code": "code 1",
            "value": 900,
            "purchase_at": "2020-08-08",
            "cpf": self.dealer.cpf
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Cadastrar uma compra de compra faltando 'purchase_code'
    def test_create_purchase_missing_purchase_code(self):
        url = reverse('core:purchase-list')
        auth = f'JWT {self.token}'
        data = {
            "value": 900,
            "purchase_at": "2020-08-08",
            "cpf": self.dealer.cpf
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Cadastrar uma compra de compra passando cpf diferente do usuário autenticado
    def test_create_purchase_cpf_diff_logged_user(self):
        url = reverse('core:purchase-list')
        auth = f'JWT {self.token}'
        data = {
            "purchase_code": "code 1",
            "value": 900,
            "purchase_at": "2020-08-08",
            "cpf": "35767856044"
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Cashback acumulado
    def test_get_acumulated_cashback(self):
        url = reverse('core:acumulated-cashback')
        auth = f'JWT {self.token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
