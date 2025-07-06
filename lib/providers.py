import requests
import json
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any

load_dotenv()

price_cache = {
    'gold': None,
    'bitcoin': None,
    'sp500': None,
}

def get_asset_price(asset_type: str) -> Optional[float]:
    """
    Get the current price for a specified asset type.
    
    Args:
        asset_type (str): Type of asset ('gold', 'bitcoin', 'sp500', etc.)
        
    Returns:
        Optional[float]: Current asset price in USD, or None if error
    """
    asset_type = asset_type.lower()

    if price_cache[asset_type] is not None:
        # don't send multiple requests to the same asset type
        # this is to prevent us from getting rate limited by the API
        return price_cache[asset_type]

    if asset_type == 'gold':
        price_cache[asset_type] = get_gold_price()
    elif asset_type in ['bitcoin', 'btc']:
        price_cache[asset_type] = get_bitcoin_price()
    elif asset_type in ['sp500', 's&p500', 'spx']:
        price_cache[asset_type] = get_sp500_price()
    else:
        print(f"Warning: Unsupported asset type '{asset_type}'")
        return None
    return price_cache[asset_type]


def get_gold_price() -> Optional[float]:
    """
    Get the current gold price from goldapi.io
    URL - https://www.goldapi.io/dashboard
        
    Returns:
        Optional[float]: Gold price in USD per ounce, or None if error
    """
    api_key = os.getenv("GOLDAPI_IO_API_KEY")
    
    if not api_key:
        print("Error: GOLDAPI_IO_API_KEY not found in environment variables")
        return None

    return make_gapi_request(api_key)


def get_bitcoin_price() -> Optional[float]:
    """
    Get the current Bitcoin price from CoinGecko API (free tier)
    
    Returns:
        Optional[float]: Bitcoin price in USD, or None if error
    """
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data['bitcoin']['usd']
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Bitcoin price: {e}")
        return None
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing Bitcoin price response: {e}")
        return None


def get_sp500_price() -> Optional[float]:
    """
    Get the current S&P 500 index value from Alpha Vantage or similar free API
    Note: This is a placeholder implementation - you'll need to add a real provider
    
    Returns:
        Optional[float]: S&P 500 index value, or None if error
    """
    # Placeholder implementation - you can integrate with Alpha Vantage, Yahoo Finance, etc.
    print("S&P 500 price fetching not yet implemented")
    print("You can add integration with Alpha Vantage, Yahoo Finance, or other providers")
    return None


def make_gapi_request(api_key: str, asset: str = "XAU") -> Optional[float]:
    """
    Make a request to the goldapi.io API to get the current gold price
    
    Args:
        api_key (str): goldapi.io API key
        asset (str): Asset symbol (default: "XAU" for gold)

    Returns:
        Optional[float]: Gold price in USD per ounce, or None if error
    """
    symbol = asset.upper()
    curr = "USD"
    date = ""

    url = f"https://www.goldapi.io/api/{symbol}/{curr}{date}"

    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        result = response.text
        return json.loads(result).get("price")
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing gold price response: {e}")
        return None
