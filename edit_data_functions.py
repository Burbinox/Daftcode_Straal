from datetime import datetime, timedelta
import requests
from decimal import Decimal


TWO_PLACES = Decimal(10) ** -2


def sort_by_date_and_change_to_proper_date_format(data):
    """
    Function sorts data by date in chronological order

    :param data: almost ready json data which will be send to user after this function
    :return: dict sorted by date
    """
    sorted_data = sorted(data, key=lambda elem: elem['date'])
    for e in data:
        e['date'] = e['date'].isoformat()
    return sorted_data


def serialize_data_in_every_object(data):
    """
    Function that unifies the date so that you can sort it chronologically later

    :param data: data from user
    :return: dict where values of "created_at" is in datetime format
    """
    for elem in data:
        for el in data[elem]:
            if el['created_at'][-1] == "Z":
                el['created_at'] = datetime.strptime(el['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                temp_data = [datetime.strptime(el['created_at'][:19], "%Y-%m-%dT%H:%M:%S"),
                             float(el['created_at'][19:].replace(":", "."))]
                el['created_at'] = temp_data[0] + timedelta(hours=temp_data[1])
    return data


def get_amount_in_pln(amount, currency):
    """
    Function which return amount multiplied by current exchange_rate of given currency

    :param amount: amount of money in given currency
    :param currency: three-letter currency code in ISO 4217 standard
    :return: amount of money in PLN
    """
    if currency == "PLN":
        return amount
    else:
        current_exchange_rate_object = requests.get(f'http://api.nbp.pl/api/exchangerates/rates/A/{currency}/')
        current_exchange_rate = current_exchange_rate_object.json()['rates'][0]['mid']
        return amount*current_exchange_rate


def check_payment_mean(payment_method, ele):
    if payment_method == "pay_by_link":
        return ele["bank"]
    elif payment_method == "dp":
        return ele["iban"]
    elif payment_method == "card":
        return ele["cardholder_name"] + " " + ele["cardholder_surname"] + " " + ele["card_number"]


def prepare_response_obj(data):
    response = []
    for elem in data:
        for el in data[elem]:
            amount_in_pln = Decimal(str(get_amount_in_pln(el['amount'], el['currency']))).quantize(TWO_PLACES)
            res_obj = {
                'date': el['created_at'],
                'type': elem,
                'payment_mean': check_payment_mean(elem, el),
                'description':  el['description'],
                'currency': el['currency'],
                'amount': el['amount'],
                'amount_in_pln': float(amount_in_pln),
            }
            response.append(res_obj)
    return response
