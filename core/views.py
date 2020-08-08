from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.models import Dealer, Purchase
from core.serializers import DealerSerializer, PurchaseSerializer


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
