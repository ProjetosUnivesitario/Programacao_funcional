import requests
from bs4 import BeautifulSoup
from functools import reduce

# Sistema de Web Scrapper e uso de programação funcional.
# Estamos usando a biblioteca requests para fazer requisições get e BeautifulSoup para trazer informações da requisição para nosso código.
# Site que estamos fazendo requisição para trazer o valores da cotação de moeda.

# exemplo de moedas para cotação KRW, INR, JPY, CAD, EUR, GBP, CNY, MXN, USD, BRL ...
coin = {"krw", "inr", "jpy", "cad", "eur", "gbp", "cny", "mxn", "usd", "brl"}

# validando informações recebidas.
def validation(currency_quote, exchange, price):
    currency_quote, exchange = currency_quote.strip().lower(), exchange.strip().lower()  # Remove espaços extras e normaliza
    if not all(map(lambda x: x, [currency_quote, exchange, price])):
        print("Preencher todos os campos")
        return client()
    if not all(isinstance(x, str) for x in [currency_quote, exchange]) or not isinstance(price, float):
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
    return lambda price: requests.get(
        f"https://wise.com/br/currency-converter/{currency_quote}-to-{exchange}-rate?amount={price}",
        headers={"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36"}
    )

# Função para buscar o valor da cotação do site usando list comprehension e reduce.
def search_conversion(response):
    site = BeautifulSoup(response.text, "html.parser")
    value = reduce(lambda _, el: el, [el.get('value') for el in site.find_all('input', id="target-input")], None)
    print(value)

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