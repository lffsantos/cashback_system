from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.models import Dealer, Purchase
from core.serializers import DealerSerializer, PurchaseSerializer


class DealerViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put']
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DealerSerializer
    queryset = Dealer.objects.all()

    # def perform_destroy(self, instance):
    #     user = instance.user
    #     instance.delete()
    #     user.delete()


class PurchaseViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put']
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
