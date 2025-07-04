import requests
from dotenv import load_dotenv
import os

load_dotenv()

def make_gapi_request():
    """
    Make a request to the goldapi.io API to get the current gold price
    Returns the gold price in USD per ounce
    URL - https://www.goldapi.io/dashboard
    """
    api_key = os.getenv("GOLDAPI_API_KEY")
    print(api_key)
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
        print(result)
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))
