import datetime
import json

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from model_bakery import baker
from parameterized import parameterized

from core.serializers import DealerSerializer, PurchaseSerializer

User = get_user_model()


class DealerSerializerTest(TestCase):

    @parameterized.expand([
        json.dumps({"cpf": "55320468083", "email": "teste@example.com", "name": "teste", "password": "123456"}),
        json.dumps({"cpf": "11111111112", "email": "teste@example.com", "name": "teste", "password": "123456"})
    ])
    def test_create_dealer(self,  payload):
        data = json.loads(payload)
        serializer = DealerSerializer(data=data)
        if not serializer.is_valid():
            self.assertEqual(serializer.errors['cpf'][0], "CPF inválido")
        else:
            serializer.create(data)
            self.assertEqual(serializer.data, {'name': 'teste', 'cpf': '55320468083', 'email': 'teste@example.com'})


class PurchaseSerializerTest(TestCase):
    def test_create_purchase(self):
        self.dealer = baker.make('Dealer', cpf='55320468083')
        payload = {"purchase_code": "code1", "value": 1000, "cpf": '55320468083'}
        client = Client()
        response = client.get("")
        request = response.wsgi_request
        request.user = User.objects.get(id=self.dealer.id)
        serializer = PurchaseSerializer(data=payload, context={'request': request})
        serializer.is_valid()
        instance = serializer.create(payload)
        expected = {
            'purchase_code': 'code1',
            'value': '1000.00',
            'purchase_at': str(datetime.date.today()),
            'status': 'Em validação',
            'cashback_percentage': '0.00', 'cashback_value': '0.00'}
        self.assertEqual(PurchaseSerializer(instance).data, expected)

    def test_create_purchase_approve_cpf(self):
        self.dealer = baker.make('Dealer', cpf='15350946056')
        payload = {"purchase_code": "code1", "value": 1000, "cpf": '15350946056'}
        client = Client()
        response = client.get("")
        request = response.wsgi_request
        request.user = User.objects.get(id=self.dealer.id)
        serializer = PurchaseSerializer(data=payload, context={'request': request})
        serializer.is_valid()
        instance = serializer.create(payload)
        expected = {
            'purchase_code': 'code1',
            'value': '1000.00',
            'purchase_at': str(datetime.date.today()),
            'status': 'Aprovado',
            'cashback_percentage': '0.00', 'cashback_value': '0.00'}
        self.assertEqual(PurchaseSerializer(instance).data, expected)
