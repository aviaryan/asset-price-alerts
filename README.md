# Asset Invest Alerts

Asset Invest Alerts is a Python tool that monitors asset prices and sends you notifications when your custom alert conditions are met. Configure your alerts in a YAML file, and let the script notify you when your targets are hit.

> This is an alternative to using **TradingView premium** for long-term investment alerts.

## Features

- Monitor prices of stocks, cryptocurrencies, gold, Nifty 50 (Indian stock market index), or other assets.
- Define custom alert conditions in a YAML file.
- Receive notifications when your alert conditions are met.
- Easily schedule the script to run automatically (e.g., daily) using `cron`.

## Supported Assets

- **Gold** - Current gold prices in USD per ounce
- **Bitcoin** - Cryptocurrency prices in USD
- **Nifty 50** - Indian stock market index (NSE) in INR
- **USD/INR** - Exchange rate (INR per USD)
- **S&P 500** - US stock market index (placeholder - needs implementation)

## Getting Started

### 1. Install Dependencies

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. To install dependencies, run:

```sh
uv sync
```

### 2. Configure Your Alerts

Copy the example alerts file and edit it to define your own alerts:

```sh
cp alerts.example.yaml alerts.yaml
```

Edit `alerts.yaml` to specify the assets and alert conditions you want to monitor. Example:

```yaml
- name: Gold Buy
  asset: gold
  price: 3200
  alert_type: price_below
- name: Bitcoin Sell
  asset: bitcoin
  price: 150000
  alert_type: price_above
- name: Nifty 50 High Alert
  asset: nifty
  price: 26000
  alert_type: price_above
- name: Nifty 50 Support Level
  asset: nifty50
  price: 24000
  alert_type: price_below
```

**Asset Types:**
- `gold` - Gold prices
- `bitcoin` or `btc` - Bitcoin prices
- `nifty`, `nifty50`, or `nifty 50` - Nifty 50 index
- `usd_inr`, `usd/inr`, `usdinr`, or `usd-inr` - USD/INR rate (INR per USD)

Set the required API keys in the `.env` file.

```sh
cp .env.example .env 
# and set goldapi.io API KEY in .env file
```

**Note:** Nifty 50 and USD/INR prices are fetched from Yahoo Finance API and don't require additional API keys.

### 3. Run the Script

To check your alerts and receive notifications, run:

```sh
uv run main.py
```

## Automate with Cron

To have the script run automatically every day (e.g., at 8:00 AM), add a crontab entry:

1. Find the full path to your Python executable (if needed):

   ```sh
   which python3
   ```

2. Edit your crontab:

   ```sh
   crontab -e
   ```

3. Add the following line to run the script every day at 11:00 AM (adjust the path and time as needed):

   ```
   0 11 * * * cd /full/path/to/repo/asset-price-alert && /full/path/to/uv run main.py
   ```

   - This assumes your project is located at `/full/path/to/repo/asset-price-alert`.
   - Make sure your `alerts.yaml` is configured and present in the project directory.

## Notifications

The script will notify you (via your configured method) if any of your alert conditions are met. Check the `lib/notify.py` file to see or customize how notifications are sent (e.g., email, desktop, etc.).
