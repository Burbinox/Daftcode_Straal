def check_if_data_is_correct(data):
    """
    Function check if data have proper format

    :param data: date from user
    :return: False if something is wrong
             None if everything is correct
    """
    list_of_allowed_keys_of_pay_by_link = ['created_at', "currency", "amount", "description", "bank"]
    list_of_allowed_keys_of_dp = ['created_at', "currency", "amount", "description", "iban"]
    list_of_allowed_keys_of_card = ['created_at', "currency", "amount", "description",
                                    "cardholder_name", "cardholder_surname", "card_number"]
    #  check if data have only allowed keys
    for elem in data:  # check every payment method
        if elem == 'pay_by_link':
            for el in data[elem]:
                for e in el.keys():
                    if e not in list_of_allowed_keys_of_pay_by_link:
                        return False
        if elem == 'dp':
            for el in data[elem]:
                for e in el.keys():
                    if e not in list_of_allowed_keys_of_dp:
                        return False
        if elem == 'card':
            for el in data[elem]:
                for e in el.keys():
                    if e not in list_of_allowed_keys_of_card:
                        return False
    # check if data have proper format
    for elem in data:  # check every payment method
        if elem == 'pay_by_link':
            for e in data[elem]:
                base_values_check(e)
                if type(e["bank"]) != str:
                    return False
        if elem == 'dp':
            for e in data[elem]:
                base_values_check(e)
                if type(e["iban"]) != str and len(e["iban"]) <= 30:
                    return False
        if elem == 'card':
            for e in data[elem]:
                base_values_check(e)
                if type(e["cardholder_name"]) != str:
                    return False
                if type(e["cardholder_surname"]) != str:
                    return False
                if type(e["card_number"]) != str and len(e["card_number"]) == 16:
                    return False


def base_values_check(payment_elem):
    """
    Function check if base values like created_at, currency, amount, description are correct

    :param payment_elem: one of pay_by_link, dp, card
    :return: False if something is wrong
             None if everything is correct
    """
    if type(payment_elem["created_at"]) != str:
        return False
    if payment_elem['currency'] not in ['EUR', 'USD', 'GBP', 'PLN']:
        return False
    if type(payment_elem["amount"]) != int:
        return False
    if type(payment_elem["description"]) != str:
        return False
