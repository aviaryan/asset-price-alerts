import logging
import os
from dotenv import load_dotenv
# own libraries
from lib.providers import get_asset_price
from lib.notify import show_notification
from lib.alerts import load_alerts, group_alerts_by_asset, get_triggered_alerts, format_alert_message

logger = logging.getLogger(__name__)

load_dotenv()

CRON_MODE = os.getenv("CRON_MODE") == "1"

def main():
    # Load alert configurations
    alerts = load_alerts("alerts.yaml")
    if not alerts:
        logger.error("No alerts configured or error loading alerts.yaml")
        return

    logger.info("Loaded %d alert(s)", len(alerts))

    # Group alerts by asset type
    alerts_by_asset = group_alerts_by_asset(alerts)
    logger.info(
        "Monitoring %d asset type(s): %s",
        len(alerts_by_asset),
        ", ".join(alerts_by_asset.keys()),
    )
    
    total_triggered = 0
    
    # Process each asset type
    for asset_type, asset_alerts in alerts_by_asset.items():
        logger.info("\n--- %s ---", asset_type.upper())
        
        # Get current price for this asset
        current_price = get_asset_price(asset_type)

        if current_price is None:
            logger.error("Failed to fetch %s price. Skipping %d alert(s).", asset_type, len(asset_alerts))
            show_notification(
                message=f"Failed to fetch {asset_type} price. Skipping {len(asset_alerts)} alert(s).",
                title="Asset Price Alert",
                subtitle=f"Please check the code for {asset_type}"
            )
            continue

        logger.info("Current %s price: $%.2f", asset_type, current_price)
        
        # Check which alerts are triggered for this asset
        triggered_alerts = get_triggered_alerts(current_price, asset_alerts)
        
        if triggered_alerts:
            logger.info("%d %s alert(s) triggered!", len(triggered_alerts), asset_type)
            total_triggered += len(triggered_alerts)
            
            # Show notifications for each triggered alert
            for alert in triggered_alerts:
                alert_message = format_alert_message(alert, current_price)
                logger.info("Alert: %s", alert_message)
                
                # Show desktop notification
                show_notification(
                    message=alert_message,
                    title="Asset Price Alert",
                    subtitle=f"{alert.get('name', 'Asset')} Alert Triggered"
                )
        else:
            logger.info("No %s alerts triggered.", asset_type)
            # Show a summary of current status for this asset
            for alert in asset_alerts:
                name = alert.get('name', 'Asset')
                threshold = alert.get('price')
                alert_type = alert.get('alert_type', 'price_below')
                logger.info(
                    "  %s: $%.2f (watching for %s $%s)",
                    name,
                    current_price,
                    alert_type,
                    threshold,
                )
    
    # Summary
    logger.info("\n=== SUMMARY ===")
    logger.info("Total alerts triggered: %d", total_triggered)
    if total_triggered == 0:
        logger.info("All monitored assets are within normal ranges.")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.WARNING if CRON_MODE else logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    main()
