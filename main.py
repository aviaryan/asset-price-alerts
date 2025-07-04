import os
from dotenv import load_dotenv
# own libraries
from lib.providers import get_asset_price
from lib.notify import show_notification
from lib.alerts import load_alerts, group_alerts_by_asset, get_triggered_alerts, format_alert_message

load_dotenv()

def main():
    # Load alert configurations
    alerts = load_alerts("alerts.yaml")
    if not alerts:
        print("No alerts configured or error loading alerts.yaml")
        return

    print(f"Loaded {len(alerts)} alert(s)")

    # Group alerts by asset type
    alerts_by_asset = group_alerts_by_asset(alerts)
    print(f"Monitoring {len(alerts_by_asset)} asset type(s): {', '.join(alerts_by_asset.keys())}")
    
    total_triggered = 0
    
    # Process each asset type
    for asset_type, asset_alerts in alerts_by_asset.items():
        print(f"\n--- {asset_type.upper()} ---")
        
        # Get current price for this asset
        current_price = get_asset_price(asset_type)

        if current_price is None:
            print(f"Failed to fetch {asset_type} price. Skipping {len(asset_alerts)} alert(s).")
            continue

        print(f'Current {asset_type} price: ${current_price:.2f}')
        
        # Check which alerts are triggered for this asset
        triggered_alerts = get_triggered_alerts(current_price, asset_alerts)
        
        if triggered_alerts:
            print(f"{len(triggered_alerts)} {asset_type} alert(s) triggered!")
            total_triggered += len(triggered_alerts)
            
            # Show notifications for each triggered alert
            for alert in triggered_alerts:
                alert_message = format_alert_message(alert, current_price)
                print(f"Alert: {alert_message}")
                
                # Show desktop notification
                show_notification(
                    message=alert_message,
                    title="Asset Price Alert",
                    subtitle=f"{alert.get('name', 'Asset')} Alert Triggered"
                )
        else:
            print(f"No {asset_type} alerts triggered.")
            # Show a summary of current status for this asset
            for alert in asset_alerts:
                name = alert.get('name', 'Asset')
                threshold = alert.get('price')
                alert_type = alert.get('alert_type', 'price_below')
                print(f"  {name}: ${current_price:.2f} (watching for {alert_type} ${threshold})")
    
    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"Total alerts triggered: {total_triggered}")
    if total_triggered == 0:
        print("All monitored assets are within normal ranges.")

if __name__ == "__main__":
    main()
