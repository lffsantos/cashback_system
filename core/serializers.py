from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.models import Dealer, Purchase
from core.validators import validate_cpf


class DealerSerializer(serializers.ModelSerializer):
    cpf = serializers.CharField(validators=[validate_cpf, UniqueValidator(queryset=Dealer.objects.all())])
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Dealer
        exclude = ['user']

    def validate_cpf(self, data):
        user = User.objects.filter(username=data)
        if user:
            raise serializers.ValidationError("Já existe usuário com esse CPF")

        return data

    def create(self, validated_data):
        username = validated_data['cpf']
        password = make_password(validated_data.pop('password'))
        user = User.objects.create(username=username, password=password)
        dealer = Dealer.objects.create(user=user, **validated_data)
        return dealer


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'
