import requests
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import QueryDict
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.models import Dealer, Purchase
from core.serializers import DealerSerializer, PurchaseSerializer
from core.validators import validate_cpf


class DealerRegisterViewSet(GenericViewSet, CreateModelMixin):
    http_method_names = ('post', )
    permission_classes = (AllowAny,)
    authentication_classes = []
    serializer_class = DealerSerializer
    queryset = Dealer.objects.all()


class PurchaseViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()

    def perform_create(self, serializer):
        # import pdb
        # pdb.set_trace()

        if not self.request.user.is_superuser:
            data = self.request.data.copy()
            data['cpf'] = self.request.user.dealer.cpf
        else:
            if 'cpf' not in self.request.data:
                raise NotAcceptable(detail="Informe um CPF!")
            try:
                is_valid_cpf = validate_cpf(self.request.data.get('cpf'))
            except Exception as error:
                print(self.request.data)
                raise Exception(error)
            data = self.request.data

        # trick for test
        if isinstance(data, QueryDict):
            data = data.dict()

        if serializer.is_valid():
            try:
                serializer.create(data)
            except ObjectDoesNotExist:
                raise ValidationError(detail="Revendedor Não cadastrado", code=400)

            return True

        return False

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Purchase.objects.all()

        try:
            dealer = self.request.user.dealer
        except ObjectDoesNotExist:
            raise NotAcceptable(detail="Usuário não é um revendedor")
        return Purchase.objects.filter(dealer=dealer)


class AcumulatedCashbackDealerViewSet(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        url = 'https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback?cpf=12312312323'
        headers = {'token': 'ZXPURQOARHiMc6Y0flhRC1LVlZQVFRnm'}
        results = requests.get(url=url, headers=headers).json()
        return Response(results)
