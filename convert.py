from currency_converter import ECB_URL, SINGLE_DAY_ECB_URL
from currency_converter import CurrencyConverter
#from datetime import date
from os import system
import requests
import json
from colorama import init, Fore, Back, Style

init(autoreset=True)
c = CurrencyConverter(ECB_URL)  # Carrega o histórico completo atualizado
c = CurrencyConverter(SINGLE_DAY_ECB_URL)  # Carrega as taxas mais recentes
system('cls')
first_date, last_date = c.bounds['USD']  # Carrega a primeira e ultima data
# Muda o formato da última data de cotação
Data_Conversao = last_date.strftime('%d/%m/%Y')
# Data_Conversao = str(last_date)
# ano = Data_Conversao[0:4]
# mes = Data_Conversao[5:7]
# dia = Data_Conversao[8:10]
# Imprime a última data que a moeda foi atualizada
moedas = c.currencies


def boas_vindas():
    print(Fore.GREEN+'''
        Bem-Vindos ao Projeto
    Sistema Conversor de Moedas
    Uso padrão internacional de moedas.
    Ex.: "USD" Dolar/Americano; "BRL" Real/Brasileiro; "ARS" Peso/Argentino e etc...
    Para finalizar digite o valor igual 0.
    ''')


def exibir_menu():
    print(Fore.RED+'''
Escolha a moeda:
[1] USD
[2] BRL
[3] OUTRA
''')
    try:
        opcao = input('Digite sua opção: ').upper()
        if opcao == '1':
            opcao = 'USD'
        elif opcao == '2':
            opcao = 'BRL'
        elif opcao == '3':
            print(Fore.RED+'Digite a moeda, com três ou quatro letras.')
            opcao = input('Para moeda: ').upper()
        opcao2 = input('Digite sua opção: ').upper()
        if opcao2 == '1':
            opcao2 = 'USD'
        elif opcao2 == '2':
            opcao2 = 'BRL'
        elif opcao2 == '3':
            print(Fore.RED+'Digite a moeda, com três ou quatro letras')
            opcao2 = input('Para moeda: ').upper()
        return(opcao, opcao2)
    except ValueError:
        print()


while True:
    try:
        boas_vindas()
        valor = float(input('Entre com um valor: ').replace(',', '.'))
        if valor == 0:
            break
    except ValueError:
        print(Fore.RED+'Favor digitar um valor válido, "NÚMERO".')
    #    valor = float(input('Entre com um valor: ').replace(',', '.'))
    else:
        opcao, opcao2 = exibir_menu()  # input('Da moeda: ').upper()
        Da_moeda = opcao
        Para_moeda = opcao2
        try:
            conversao = c.convert(valor, Da_moeda, Para_moeda)
            print(Fore.MAGENTA + f'Data da Cotação: {Data_Conversao}')
            print(
                Fore.BLUE+f' {valor:,.2f} {Da_moeda} = {conversao:,.2f} {Para_moeda}')
        except ValueError:
            requisicao = requests.get(
                'https://economia.awesomeapi.com.br/json/all')
            cotacao = requisicao.json()
            # list_moedas = ['USD', 'USDT', 'CAD', 'GBP', 'ARS', 'BTC', 'LTC',
            #               'EUR', 'JPY', 'CHF', 'AUD', 'CNY', 'ILS', 'ETH', 'XRP', 'DOGE']
            try:
                moeda = cotacao[Da_moeda]['code']
                moeda1 = cotacao[Da_moeda]['codein']
                v1 = float(cotacao[Da_moeda]['bid'])
                vt = valor*v1
                # vt1 = valor/v1
                print(Fore.MAGENTA+f'Data da Cotação:  {Data_Conversao}')
                print(
                    Fore.BLUE+f'{valor:,.2f} {Da_moeda} = {vt:,.2f} {Para_moeda}')
            except KeyError:
                print(Fore.YELLOW+'Voce deve selecionar as moedas para conversão!')
        except KeyError:
            print(Fore.RED+'Não encontou!')
