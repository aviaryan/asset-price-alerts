import logging
import yaml
from typing import List, Dict, Any
from collections import defaultdict


logger = logging.getLogger(__name__)


def load_alerts(file_path: str = "alerts.yaml") -> List[Dict[str, Any]]:
    """
    Load alerts from a YAML file.
    
    Args:
        file_path (str): Path to the YAML alerts file
        
    Returns:
        List[Dict[str, Any]]: List of alert configurations
    """
    try:
        with open(file_path, 'r') as file:
            alerts = yaml.safe_load(file)
            return alerts if alerts else []
    except FileNotFoundError:
        logger.error("Alert file '%s' not found.", file_path)
        return []
    except yaml.YAMLError as e:
        logger.error("Error parsing YAML file: %s", e)
        return []


def group_alerts_by_asset(alerts: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group alerts by asset type.
    
    Args:
        alerts (List[Dict[str, Any]]): List of alert configurations
        
    Returns:
        Dict[str, List[Dict[str, Any]]]: Dictionary with asset types as keys and alerts as values
    """
    grouped = defaultdict(list)
    
    for alert in alerts:
        asset = alert.get('asset', None)
        if asset is None:
            logger.warning("Alert '%s' has no asset type", alert.get('name', 'Unknown'))
            continue
        grouped[asset].append(alert)

    return dict(grouped)


def check_alert_condition(current_price: float, alert: Dict[str, Any]) -> bool:
    """
    Check if an alert condition is met.
    
    Args:
        current_price (float): The current asset price
        alert (Dict[str, Any]): Alert configuration containing 'price', 'alert_type', etc.
        
    Returns:
        bool: True if alert condition is met, False otherwise
    """
    if current_price is None:
        return False
    
    threshold_price = alert.get('price')
    alert_type = alert.get('alert_type', 'price_below')
    
    if threshold_price is None:
        logger.warning("Alert '%s' has no price threshold", alert.get('name', 'Unknown'))
        return False
    
    if alert_type == 'price_below':
        return current_price < threshold_price
    elif alert_type == 'price_above':
        return current_price > threshold_price
    elif alert_type == 'price_equal':
        # Allow for small floating point differences
        return abs(current_price - threshold_price) < 0.01
    else:
        logger.warning("Unknown alert type '%s' for alert '%s'", alert_type, alert.get('name', 'Unknown'))
        return False


def get_triggered_alerts(current_price: float, alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Get all alerts that are currently triggered for a specific asset.
    
    Args:
        current_price (float): The current asset price
        alerts (List[Dict[str, Any]]): List of alert configurations for this asset
        
    Returns:
        List[Dict[str, Any]]: List of triggered alerts
    """
    triggered = []
    
    for alert in alerts:
        if check_alert_condition(current_price, alert):
            triggered.append(alert)
    
    return triggered


def format_alert_message(alert: Dict[str, Any], current_price: float) -> str:
    """
    Format a notification message for an alert.
    
    Args:
        alert (Dict[str, Any]): Alert configuration
        current_price (float): Current asset price
        
    Returns:
        str: Formatted alert message
    """
    name = alert.get('name', 'Asset')
    threshold = alert.get('price')
    alert_type = alert.get('alert_type', 'price_below')
    asset = alert.get('asset', 'unknown').title()
    
    if alert_type == 'price_below':
        condition = f"below ${threshold}"
    elif alert_type == 'price_above':
        condition = f"above ${threshold}"
    elif alert_type == 'price_equal':
        condition = f"equal to ${threshold}"
    else:
        condition = f"meeting condition (${threshold})"
    
    return f"{name}: {asset} is now ${current_price:.2f} - {condition}!"
