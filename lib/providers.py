import requests
import json
import os
from typing import Optional, Dict, Any


def get_asset_price(asset_type: str, api_key: str = None) -> Optional[float]:
    """
    Get the current price for a specified asset type.
    
    Args:
        asset_type (str): Type of asset ('gold', 'bitcoin', 'sp500', etc.)
        api_key (str): API key for the provider (if required)
        
    Returns:
        Optional[float]: Current asset price in USD, or None if error
    """
    asset_type = asset_type.lower()
    
    if asset_type == 'gold':
        return get_gold_price(api_key)
    elif asset_type in ['bitcoin', 'btc']:
        return get_bitcoin_price()
    elif asset_type in ['sp500', 's&p500', 'spx']:
        return get_sp500_price()
    else:
        print(f"Warning: Unsupported asset type '{asset_type}'")
        return None


def get_gold_price(api_key: str = None) -> Optional[float]:
    """
    Get the current gold price from goldapi.io
    
    Args:
        api_key (str): goldapi.io API key
        
    Returns:
        Optional[float]: Gold price in USD per ounce, or None if error
    """
    if not api_key:
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


def make_gapi_request(api_key: str) -> Optional[float]:
    """
    Make a request to the goldapi.io API to get the current gold price
    
    Args:
        api_key (str): goldapi.io API key
        
    Returns:
        Optional[float]: Gold price in USD per ounce, or None if error
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


# Legacy function for backward compatibility
def get_gold_price_legacy():
    """Legacy function - use get_asset_price('gold') instead"""
    return get_gold_price()
