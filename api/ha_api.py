import requests

from ..crud import state

from .keys_etc import HA_TOKEN

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "content-type": "application/json",
}


def get_data_from_api(api_url, storage_dictionary, store_key, values, lookup_key, default):
    try:
        response = requests.get(api_url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            current_value = data.get(lookup_key, default)
            if values[3] in ["number", "graph"]:
                current_value = float(current_value)
                output_dictionary = {
                    "name": values[0],
                    "value": current_value,
                    "units": values[2],
                    "type": values[3],
                    "min": values[4],
                    "max": values[5]
                }
            storage_dictionary[store_key] = output_dictionary
        else:
            error_status_code_message = "Error: " + str(response.status_code)
            print(error_status_code_message)
            return None

        response.close()
        return storage_dictionary

    except Exception as e:
        print(f"Error fetching data - {e}")


def get_ha_api_data(db):
    api_data = state.get_ha_api_values(db)
    ha_data = {}
    api_url = api_data["api_url"][1]
    for key, value in api_data.items():
        if key != "api_url":
            if value[0] != "":
                current_api_url = f"{api_url}{value[1]}"
                get_data_from_api(current_api_url, ha_data, key, value, "state", "0")
    return ha_data
