from .general import timeit
from constants import *
from objects import Database, Product

import requests
import json


@timeit
def get_user_info(variables, sender_id):
    url = variables[FB_GRAPH_URL].format(sender_id, variables[PAGE_ACCESS_TOKEN])
    r = requests.get(url)
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        print(r.text)


@timeit
def send_message(recipient_id, message_text, variables):
    multi_message = message_text.split("\n")
    for message in multi_message:
        if len(message) > 0:
            data = json.dumps({"recipient": {"id": recipient_id}, "message": {"text": message.format()}})
            params["access_token"] = variables[PAGE_ACCESS_TOKEN]
            url = variables[FB_MESSAGES_URL].format(variables[FB_API_VERSION])
            r = requests.post(url=url, params=params, headers=headers, data=data)
            print(r.text)



@timeit
def send_attachment(recipient_id, _message, variables):
    data = json.dumps({"recipient": {"id": recipient_id}, "message": _message})
    url = variables[FB_MESSAGES_URL].format(variables[FB_API_VERSION])
    params["access_token"] = variables[PAGE_ACCESS_TOKEN]
    r = requests.post(url=url, params=params, headers=headers, data=data)
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        print(r.text)


@timeit
def send_products(variables, _sender_id, _db=Database(), store_id: str = "5edd1bd2c8f52c4620becb3a"):
    elements = []
    prds = _db.get_schema().products.find({"store": store_id})
    for elem in prds:
        elem = Product(**elem)
        elements.append(elem.get_element())

    payload = {"template_type": "generic", "elements": elements}
    attachment = {"type": "template", "payload": payload}
    response = {"attachment": attachment}
    # send_message(_sender_id, get_speech("product_list"))
    send_attachment(recipient_id=_sender_id, _message=response, variables=variables)
