
from django.core.exceptions import ValidationError, ObjectDoesNotExist


def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError('Cpf deve conter somente dígitos')

    if len(value) != 11:
        raise ValidationError('CPF deve conter 11 dígitos')

    numbers = [int(digit) for digit in value]

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        raise ValidationError('CPF inválido')

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        raise ValidationError('CPF inválido')


def validate_dealer(value):
    from core.models import Dealer
    try:
        dealer = Dealer.objects.get(cpf=value)
    except ObjectDoesNotExist:
        raise ValidationError('Não existe revendedor cadastrado com esse CPF!')

