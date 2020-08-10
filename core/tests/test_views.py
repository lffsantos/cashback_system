import datetime
from unittest import TestCase

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt.settings import api_settings

from core.models import Dealer, dealer

User = get_user_model()


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

    # Cadastro de compra com usuário revendedor
    def test_create_purchase_valid(self):
        url = reverse('core:purchase-list')
        auth = f'JWT {self.token}'
        data = {
            "purchase_code": "code 1",
            "value": 900,
            'purchase_at': str(datetime.date.today()),
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Cadastro de compra com usuário admin
    def test_create_purchase_valid_admin(self):
        self.user = baker.make('CashBackUser', email="testex@gmail.com", is_superuser=True)
        self.jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        self.jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = self.jwt_payload_handler(self.user)
        auth = f'JWT {self.jwt_encode_handler(payload)}'
        url = reverse('core:purchase-list')
        data = {
            "cpf": "25020115070",
            "purchase_code": "code 1",
            "value": 900,
            'purchase_at': str(datetime.date.today()),
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Cadastro de compra com usuário admin sem cpf
    def test_create_purchase_no_cpf_admin(self):
        self.user = baker.make('CashBackUser', email="testex@gmail.com", is_superuser=True)
        self.jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        self.jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = self.jwt_payload_handler(self.user)
        auth = f'JWT {self.jwt_encode_handler(payload)}'
        url = reverse('core:purchase-list')
        data = {
            "purchase_code": "code 1",
            "value": 900,
            'purchase_at': str(datetime.date.today()),
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Cadastro de compra com usuário admin cpf invalido
    def test_create_purchase_invalid_cpf_admin(self):
        self.user = baker.make('CashBackUser', email="testex@gmail.com", is_superuser=True)
        self.jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        self.jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = self.jwt_payload_handler(self.user)
        auth = f'JWT {self.jwt_encode_handler(payload)}'
        url = reverse('core:purchase-list')
        data = {
            "cpf": "25020115011",
            "purchase_code": "code 1",
            "value": 900,
            'purchase_at': str(datetime.date.today()),
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Cadastro de compra com usuário admin cpf não cadastrado
    def test_create_purchase_no_cpf_dealer_admin(self):
        self.user = baker.make('CashBackUser', email="testex@gmail.com", is_superuser=True)
        self.jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        self.jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = self.jwt_payload_handler(self.user)
        auth = f'JWT {self.jwt_encode_handler(payload)}'
        url = reverse('core:purchase-list')
        data = {
            "cpf": "17890466021",
            "purchase_code": "code 1",
            "value": 900,
            'purchase_at': str(datetime.date.today()),
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Lista todas as compras quando o usuário autenticado é admin
    def test_list_purchase_admin_user(self):
        self.dealer1 = baker.make('Dealer', cpf='55320468083')
        self.user = baker.make('CashBackUser', email="testex@gmail.com", is_superuser=True)
        baker.make('Purchase', dealer=self.dealer1)
        baker.make('Purchase', dealer=self.dealer)
        self.jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        self.jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = self.jwt_payload_handler(self.user)
        auth = f'JWT {self.jwt_encode_handler(payload)}'
        url = reverse('core:purchase-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # Lista somente as compras do usuário autenticado
    def test_list_purchase_dealer_user(self):
        self.dealer1 = baker.make('Dealer', cpf='55320468083')
        baker.make('Purchase', dealer=self.dealer1)
        baker.make('Purchase', dealer=self.dealer)
        url = reverse('core:purchase-list')
        auth = f'JWT {self.token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    # Cadastrar uma compra de compra faltando 'purchase_code'
    def test_create_purchase_missing_purchase_code(self):
        url = reverse('core:purchase-list')
        auth = f'JWT {self.token}'
        data = {
            "value": 900,
            'purchase_at': str(datetime.date.today()),
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Cashback acumulado
    def test_get_acumulated_cashback(self):
        url = reverse('core:acumulated-cashback')
        auth = f'JWT {self.token}'
        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
