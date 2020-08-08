
from django.core.exceptions import ValidationError


error_messages = {
    'invalid': 'O cpf informado é inválido',
    'digits_only': 'Digite apenas números',
    'max_digits': 'O limite de caracteres foi excedido',
}


def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError('CPF should have only numbers.')

    if len(value) != 11:
        raise ValidationError('CPF must be contains 11 digits')

    numbers = [int(digit) for digit in value]

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        raise ValidationError('CPF is not valid.')

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        raise ValidationError('CPF is not valid.')
