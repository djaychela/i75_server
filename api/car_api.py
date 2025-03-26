import requests

from ..crud import state

from .keys_etc import HA_TOKEN

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "content-type": "application/json",
}


def get_data_from_api(api_url, storage_dictionary, store_key, lookup_key, default):
    try:
        response = requests.get(api_url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            storage_dictionary[store_key] = data.get(lookup_key, default)
        else:
            error_status_code_message = "Error: " + str(response.status_code)
            print(error_status_code_message)
            return None

        response.close()
        return storage_dictionary

    except Exception as e:
        print(f"Error fetching data - {e}")


def get_car_api_data(db):
    api_data = state.get_car_api_values(db)
    car_data = {}
    battery_api_url = f"{api_data['ha_base_url']}{api_data['battery_api_url']}"
    charger_url = f"{api_data['ha_base_url']}{api_data['charger_url']}"
    charging_api_url = f"{api_data['ha_base_url']}{api_data['charging_api_url']}"
    charger_rate_url = f"{api_data['ha_base_url']}{api_data['charger_rate_url']}"
    get_data_from_api(battery_api_url, car_data, "battery_percentage", "state", "0")
    get_data_from_api(charging_api_url, car_data, "charging_state", "state", "off")
    get_data_from_api(charger_url, car_data, "charger_state", "state", "0")
    get_data_from_api(charger_rate_url, car_data, "charger_rate", "state", "0")
    get_data_from_api(battery_api_url, car_data, "attributes", "attributes", "0")

    print(f"{car_data=}")

    return car_data
