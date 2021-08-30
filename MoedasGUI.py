import PySimpleGUI as sg
from currency_converter import ECB_URL, SINGLE_DAY_ECB_URL
from currency_converter import CurrencyConverter
from os import system
import requests
import json

c = CurrencyConverter(ECB_URL)  # Carrega o histórico completo atualizado
c = CurrencyConverter(SINGLE_DAY_ECB_URL)  # Carrega as taxas mais recentes
system('cls')
first_date, last_date = c.bounds['USD']  # Carrega a primeira e ultima data
# Muda o formato da última data de cotação
Data_Conversao = last_date.strftime('%d/%m/%Y')
moedas = c.currencies

# Lista de Moedas
list_moedas = ['USD', 'USDT', 'BRL', 'CAD', 'GBP', 'ARS', 'BTC', 'LTC', 'SGD',
               'EUR', 'JPY', 'CHF', 'AUD', 'CNY', 'ILS', 'ETH', 'XRP', 'DOGE']

list_moedas1 = ['USD', 'BRL', 'CAD', 'GBP', 'BTC', 'LTC', 'ZAR', 'ISK', 'CZK',
                'SEK', 'MXN', 'HUF', 'INR', 'MYR', 'DKK', 'TRY', 'BGN', 'IDR',
                'RUB', 'RON', 'HKD', 'THB', 'PLN', 'SGD', 'KRW', 'NOK', 'PHP',
                'EUR', 'JPY', 'CHF', 'AUD', 'CNY', 'ILS', 'NZD']
"""
# Ordena crescente a listra
l = sorted(list_moedas1)
print(l)
"""


class Conversor_moedas():
    def __init__(self):
        sg.theme('Dark Blue')
    # Layout
        layout = [
            [sg.Text('Valor:', size=(5, 1)),
             sg.Input(key='valor', size=(11, 1))],
            [sg.Text('Selecione a Moedas desejada.')],
            [sg.Text('Da_Moeda:', size=(10, 1)), sg.Combo(sorted(list_moedas), size=(8, 1), default_value='USD', key='moeda'),
             sg.Text('Para_Moeda:', size=(11, 1)), sg.Combo(sorted(list_moedas1), size=(8, 1), default_value='BRL', key='moeda1')],
            [sg.Output(size=(50, 10), key='_output_')],
            [sg.Button('Limpar', button_color=('black', 'green')), sg.Button(
                'Converter', button_color=('black', 'red')), sg.Button('Sair')]
        ]
    # Declarar Janela
        self.janela = sg.Window('Conversor de Moedas', layout, font=11)

    def limpar(self):
        self.janela['valor'].update('')
        self.janela['valor'].SetFocus()
        return

    def conversao_moeda(self, valor, moeda, moeda1):
        moeda = moeda.upper()
        moeda1 = moeda1.upper()
        try:
            conversao = c.convert(valor, moeda, moeda1)
            print(f'Data da Cotação: {Data_Conversao}')
            print(f' {valor:,.2f} {moeda} = {conversao:,.2f} {moeda1}')

        except ValueError:
            requisicao = requests.get(
                'https://economia.awesomeapi.com.br/json/all')
            cotacao = requisicao.json()
            try:
                moeda = cotacao[moeda]['code']
                moeda1 = cotacao[moeda]['codein']
                v1 = float(cotacao[moeda]['bid'])
                vt = valor*v1
                print(f'Data da Cotação:  {Data_Conversao}')
                print(f'{valor:,.2f} {moeda} = {vt:,.2f} {moeda1}')

            except KeyError:
                print('Voce deve selecionar as moedas para conversão!')
        except KeyError:
            print('Não encontou!')

    def Iniciar(self):
        sg.popup_no_titlebar('''Bem_Vindos
        Projeto #08 - Sistema de Conversor Universal de Moedas.
        Converte o valor de uma moeda para outra, utilizando o padrão internacional de moedas tendo como base USD-BRL. Em Feriados, Sábado ou Domingo, a data de conversão será do último dia útil.''', background_color='black', font=12, text_color='green')

        while True:
            # Ler as informações da janela
            evento, valores = self.janela.read()
            v = self.janela['valor'].get()
            moeda = self.janela['moeda'].get()
            moeda1 = self.janela['moeda1'].get()
            if evento == sg.WINDOW_CLOSED:
                break
            elif evento == 'Sair':
                sg.popup_no_titlebar(
                    'Volte sempre!', font='18', text_color='blue')
                self.janela.close()
            elif evento == 'Converter':
                try:
                    valor = float(v.replace(',', '.'))
                    if type(valor) == float:
                        self.conversao_moeda(valor, moeda, moeda1)
                except ValueError:
                    print('Favor digitar um valor válido, "NÚMERO".')
            elif evento == 'Limpar':
                self.limpar()
                self.janela['_output_'].update('')


user = Conversor_moedas()
user.Iniciar()
