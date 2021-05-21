import json

from main import app

client = app.test_client()


# check if returned object is correct and if status code is correct
def test_report():
    data = {
        "pay_by_link": [
            {
                "created_at": "2021-05-13T01:01:43-8:00",
                "currency": "EUR",
                "amount": 3000,
                "description": "Abonament na siłownię",
                "bank": "mbank"
            }
        ],
    }
    response = client.post("/report", data=json.dumps(data), headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    assert response.json == {
        "Response": [
            {
                "amount": 3000,
                "amount_in_pln": 13487.4,
                "currency": "EUR",
                "date": "2021-05-12T17:01:43",
                "description": "Abonament na siłownię",
                "payment_mean": "mbank",
                "type": "pay_by_link"
            }]}


# check if app return 400 when headers "Content-Type" is not "application/json"
def test_report_2():
    data = {
        "pay_by_link": [
            {
                "created_at": "2021-05-13T01:01:43-8:00",
                "currency": "EUR",
                "amount": 3000,
                "description": "Abonament na siłownię",
                "bank": "mbank"
            }
        ],
    }
    response = client.post("/report", data=json.dumps(data))
    assert response.status_code == 400


# check if app return 400 when currency is wrong
def test_report_3():
    data = {
        "pay_by_link": [
            {
                "created_at": "2021-05-13T01:01:43-8:00",
                "currency": "NOGA",
                "amount": 3000,
                "description": "Abonament na siłownię",
                "bank": "mbank"
            }
        ],
    }
    response = client.post("/report", data=json.dumps(data))
    assert response.status_code == 400


