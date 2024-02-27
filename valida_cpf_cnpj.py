import functions_framework
import json
import re


@functions_framework.http
def valida_id(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if "PF" in request_json['customer_type']:
        cpf_raw = request_json['customer_id']
        cpf_raw = re.sub('[^0-9]', '', cpf_raw)
        if len(cpf_raw) != 11:
            return ("Invalid Request, CPF does not have 11 numbers", 400)
        if valida_cpf(cpf_raw) == "cpf valido":
            return 'CPF válido', 200
        else:
            return 'CPF inválido', 400

    elif "PJ" in request_json['customer_type']:
        cnpj_raw = request_json['customer_id']
        cnpj_raw = re.sub('[^0-9]', '', cnpj_raw)
        if len(cnpj_raw) != 14:
            return ("Invalid Request, CNPJ does not have 14 numbers", 400)
        if valida_cnpj(cnpj_raw) == "cnpj valido":
            return 'CNPJ valido', 200
        else:
            return 'CNPJ invalido', 400

    else:
        return "Invalid Request. Invalid customer type.", 400


def valida_cpf(cpf):
    # Calcular o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = (soma * 10) % 11
    digito_verificador1 = 0 if resto == 10 else resto
    # Calcular o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = (soma * 10) % 11
    digito_verificador2 = 0 if resto == 10 else resto
    # Verificar se os dígitos verificadores são válidos
    if int(cpf[9]) == digito_verificador1 and int(cpf[10]) == digito_verificador2:
        cpf = "cpf valido"
        return cpf
    else:
        cpf = "cpf invalido"
        return cpf


# BLOCO DE VERIFICAÇÃO PJ
def valida_cnpj(cnpj):
    # Calcular o primeiro dígito verificador
    soma = 0
    peso = 5
    for i in range(12):
        soma += int(cnpj[i]) * peso
        peso = 9 if peso == 2 else peso - 1
    resto = soma % 11
    digito_verificador1 = 0 if resto < 2 else 11 - resto
    # Calcular o segundo dígito verificador
    soma = 0
    peso = 6
    for i in range(13):
        soma += int(cnpj[i]) * peso
        peso = 9 if peso == 2 else peso - 1
    resto = soma % 11
    digito_verificador2 = 0 if resto < 2 else 11 - resto
    # Verificar se os dígitos verificadores são válidos
    if int(cnpj[12]) == digito_verificador1 and int(cnpj[13]) == digito_verificador2:
        cnpj = "cnpj valido"
        return cnpj
    else:
        cnpj = "cnpj invalido"
        return cnpj
