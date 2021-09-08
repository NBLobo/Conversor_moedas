from currency_converter import ECB_URL, SINGLE_DAY_ECB_URL
from currency_converter import CurrencyConverter
from datetime import date
import os
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

moedas = c.currencies


def boas_vindas():
    print(f'''{Fore.GREEN}+Bem-Vindos ao Projeto.{os.linesep}Sistema Conversor de Moedas
    Uso padrão internacional de moedas.{os.linesep}Ex.: "USD" Dolar/Americano; "BRL" Real/Brasileiro; "ARS" Peso/Argentino e etc...
    Para finalizar digite o valor igual 0.''')


def exibir_menu():
    print(
        f'''{Fore.RED}+Escolha a moeda:{os.linesep}[1] USD{os.linesep}[2] BRL{os.linesep}[3] OUTRA''')
    try:
        opcao = input('Digite a moeda inicial de câmbio: ').upper()
        opcao = receber_opcao_de_conversao(opcao)
        opcao2 = input('Digite a moeda de câmbio: ').upper()
        opcao2 = receber_opcao_de_conversao(opcao2)
        return(opcao, opcao2)
    except ValueError:
        print()


def receber_opcao_de_conversao(opcao):
    if opcao == '1':
        opcao = 'USD'
    elif opcao == '2':
        opcao = 'BRL'
    elif opcao == '3':
        print(Fore.RED+'Digite a moeda, com três ou quatro letras.')
        opcao = input('Para moeda: ').upper()
    return opcao


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
        moeda_inicial = opcao
        moeda_cambio = opcao2
        try:
            conversao = c.convert(valor, moeda_inicial, moeda_cambio)
            print(Fore.MAGENTA + f'Data da Cotação: {Data_Conversao}')
            print(
                Fore.BLUE+f' {valor:,.2f} {moeda_inicial} = {conversao:,.2f} {moeda_cambio}')
        except ValueError:
            requisicao = requests.get(
                'https://economia.awesomeapi.com.br/json/all')
            cotacao = requisicao.json()

            # list_moedas = ['USD', 'USDT', 'CAD', 'GBP', 'ARS', 'BTC', 'LTC',
            #               'EUR', 'JPY', 'CHF', 'AUD', 'CNY', 'ILS', 'ETH', 'XRP', 'DOGE']
            try:
                moeda_inicial = cotacao[moeda_inicial]['code']
                moeda_cambio = cotacao[moeda_inicial]['codein']
                v1 = float(cotacao[moeda_inicial]['bid'])
                vt = valor*v1
                # vt1 = valor/v1
                print(Fore.MAGENTA+f'Data da Cotação:  {Data_Conversao}')
                print(
                    Fore.BLUE+f'{valor:,.2f} {moeda_inicial} = {vt:,.2f} {moeda_cambio}')
            except KeyError:
                print(Fore.YELLOW+'Voce deve selecionar as moedas para conversão!')
        except KeyError:
            print(Fore.RED+'Não encontou!')
