import requests
import json
from config import SUBDOMAIN, ACCESS_TOKEN
def create_lead(
    name, price, product_url, size, color, delivery_type,
    first_name, last_name, phone, address,date
):


    url = f"https://{SUBDOMAIN}.amocrm.ru/api/v4/leads"

    data = [
        {
            "name": name,
            "price": int(price),
            "pipeline_id": 9150610,
            "status_id": 73560050,
            "custom_fields_values": [
                {"field_id": 887441, "values": [{"value": str(last_name)}]},
                {"field_id": 887439, "values": [{"value": str(first_name)}]},
                {"field_id": 886967, "values": [{"value": str(product_url)}]},
                {"field_id": 886969, "values": [{"value": str(size)}]},
                {"field_id": 886971, "values": [{"value": str(color)}]},
                {"field_id": 886973, "values": [{"value": str(delivery_type)}]},
                {"field_id": 886975, "values": [{"value": str(phone)}]},
                {"field_id": 886977, "values": [{"value": str(address)}]},
                {"field_id": 891021, "values": [{"value": str(date)}]},
            ],
        }
    ]

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200 or response.status_code == 201:
        print("Сделка успешно создана!")
        print("Ответ:", response.json())
    else:
        print(f"Ошибка {response.status_code}: {response.text}")
