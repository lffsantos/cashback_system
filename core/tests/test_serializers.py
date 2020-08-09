import json

import pytest
from django.test import TestCase
from model_bakery import baker
from parameterized import parameterized

from core.models import Dealer


@pytest.mark.django_db
class DealerModelTest(TestCase):
    # def setUp(self):
    #     self.cpf="55320468083"
    #     self.user = baker.make('User', username=self.cpf)


    @parameterized.expand([
        # json.dumps({"cpf": "55320468083", "email": "teste@example.com", "name": "teste", "password": "123456"}),
        json.dumps({"cpf": "000", "email": "teste@example.com", "name": "teste", "password": "123456"})
    ])
    def test_create_dealer(self,  payload):
        payload = json.loads(payload)
        print(payload)
        dealer = Dealer.objects.create_dealer(**payload)
        dealer.save()
        print(dealer.cpf)
        print(Dealer.objects.all())
        self.assertTrue(False)




