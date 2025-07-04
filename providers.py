import requests
import json

def make_gapi_request(api_key):
    """
    Make a request to the goldapi.io API to get the current gold price
    Returns the gold price in USD per ounce
    URL - https://www.goldapi.io/dashboard
    """
    symbol = "XAU"
    curr = "USD"
    date = ""

    url = f"https://www.goldapi.io/api/{symbol}/{curr}{date}"

    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        result = response.text
        return json.loads(result).get("price")
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))
        raise e
