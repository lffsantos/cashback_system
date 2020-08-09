from rest_framework import serializers

from cashback_system.settings import APRROVED_CPFS
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
    cpf = serializers.CharField(write_only=True, validators=[validate_cpf, validate_dealer], max_length=11, min_length=11)
    status = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    def validate_cpf(self, cpf):
        if cpf != self.context['request'].user.dealer.cpf:
            raise serializers.ValidationError("CPF do revendedor incorreto!")

        return cpf

    def create(self, validated_data):
        cpf = validated_data.pop('cpf')
        validated_data['status'] = Purchase.APRROVED if cpf in APRROVED_CPFS else Purchase.IN_VALIDATION
        dealer = Dealer.objects.get(cpf=cpf)
        purchase = Purchase.objects.create(dealer=dealer, **validated_data)
        return purchase

    class Meta:
        model = Purchase
        fields = ('purchase_code', 'value', 'purchase_at', 'cpf', 'status', 'cashback_percentage', 'cashback_value')

