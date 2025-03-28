import requests
from bs4 import BeautifulSoup
from functools import reduce

# Sistema de Web Scrapper e uso de programação funcional.
# Estamos usando a biblioteca requests para fazer requisições get e BeautifulSoup para trazer informações da requisição para nosso código.
# Site que estamos fazendo requisição para trazer o valores da cotação de moeda.

# exemplo de moedas para cotação KRW, INR, JPY, CAD, EUR, GBP, CNY, MXN, USD, BRL ...
coin = {"krw", "inr", "jpy", "cad", "eur", "gbp", "cny", "mxn", "usd", "brl"}

# validando informações recebidas.
# Valida se foi preenchido corretamente todos os campos, valida se o tipos estão de acordos se o moeda de origem e de destino estão de acordo com o conjunto e verifica se as moedas são divergente para poder fazer o calculo de conversão.


def validation(currency_quote, exchange, price):
    if not currency_quote or not exchange or not price:
        print("Preencher todos os campos")
        return client()
    if not isinstance(currency_quote, str) or not isinstance(exchange, str) or not isinstance(price, float):
        print("campos inválidos preencha corretamente")
        return client()
    if currency_quote not in coin:
        print(f"Moeda de origem digitada inválida, {', '.join(coin)}")
        return client()
    if exchange not in coin:
        print(f"Moeda de destino digitada inválida, {', '.join(coin)}")
        return client()
    if exchange == currency_quote:
        print("Moeda de destino e origem não pode ser iguais")
        return client()
    return currency_quote, exchange, price


# requisição get para site de cotação ainda em desenvolvimento.
def currency_converter(currency_quote, exchange):
    def get_value(price):
        # configurar o headers para requisição get do requests.
        headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36"}
        link = f"https://wise.com/br/currency-converter/{currency_quote}-to-{exchange}-rate?amount={price}"
        requisicao = requests.get(link, headers=headers)
        return requisicao
    return get_value


# Função para separar atividades no caso do BeatifulSoup para deixar o webscrapper mais organizado e buscar o valor da cotação do site.
# Só que podemos aplicar reduce com lambda e trocar find para conseguir atender as atividades propostas
def search_conversion(response):
    site = BeautifulSoup(response.text, "html.parser")
    value = site.find('input', id="target-input")
    print(value.get('value'))


# O cliente chamando a requisição especificando as inputs a seguir para personalizar a requests.
def client():
    currency_quote = input("Qual moeda para cotação?").lower()
    exchange = input("Qual a moeda de conversão?").lower()
    price = float(input("Qual valor para conversão?"))
    validation(currency_quote, exchange, price)
    teste = currency_converter(currency_quote, exchange)
    response = teste(price)
    search_conversion(response)


client()
