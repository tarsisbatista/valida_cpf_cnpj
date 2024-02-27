import functions_framework
import json
import re


@functions_framework.http
def valida_id(request):

  request_json = request.get_json(silent=True)
  request_args = request.args


  if "PF" in request_json['customer_type']:
      cpf = request_json['customer_id']
      valida_cpf(cpf)
  elif "PJ" in request_json['customer_type']:
      cnpj = request_json['customer_id']
      valida_cnpj(cnpj)
  else:
      return "Invalid Request. Invalid customer type.", 400


def valida_cpf(cpf):
    cpf = re.sub('[^0-9]', '', cpf)
    if len(cpf) != 11:
        return "Invalid Request, CPF does not have 11 numbers", 400
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
        return "CPF válido.", 200
    else:
        return "CPF inválido.", 400


 #BLOCO DE VERIFICAÇÃO PJ
def valida_cnpj(cnpj):
    cnpj = re.sub('[^0-9]', '', cnpj)
    if len(cnpj) != 14:
        return "Invalid Request, CNPJ does not have 14 numbers", 400
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
        return "CNPJ VÁLIDO.", 200
    else:
        return "CNPJ INVÁLIDO.", 400