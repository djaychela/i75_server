from collections import namedtuple

def build_api_namedtuple(current_settings_dict):
    ApiValues = namedtuple("ApiValues", ["description", "name", "value"])
    settings_to_extract = {
        "Base URL of Home Assistant": "ha_base_url",
        "Car Battery Sensor in HA": "battery_api_url",
        "Zappi Plug Status in HA": "zappi_url",
        "Car Charging Binary Sensor in HA": "charging_api_url",
        "Zappi Home Power Charging in HA": "zappi_rate_url",
    }

    api_base_values = [ApiValues(key, value, current_settings_dict[value]) for key, value in settings_to_extract.items()]

    return api_base_values