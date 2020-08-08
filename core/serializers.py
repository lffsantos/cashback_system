from rest_framework import serializers

from core.models import Dealer, Purchase
from core.validators import validate_cpf, validate_dealer


class DealerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Dealer
        fields = ('id', 'name', 'cpf', 'email', 'password')

    def create(self, validated_data):
        email, name = validated_data['email'], validated_data['name']
        cpf, password = validated_data['cpf'], validated_data['password']
        dealer = Dealer.objects.create_dealer(email=email, name=name, cpf=cpf, password=password)
        return dealer


class PurchaseSerializer(serializers.ModelSerializer):
    purchase_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='YYYY-MM-DD h:m:s')
    cpf = serializers.CharField(validators=[validate_cpf, validate_dealer], max_length=11, min_length=11)

    def create(self, validated_data):
        cpf = validated_data.pop('cpf')
        dealer = Dealer.objects.get(cpf=cpf)
        purchase = Purchase.objects.create(dealer=dealer, **validated_data)
        return purchase

    class Meta:
        model = Purchase
        fields = ('purchase_code', 'value', 'purchase_at', 'cpf')

