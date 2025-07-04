from providers import make_gapi_request


def main():
    print("Hello from asset-price-alert!")


def get_gold_price():
    return make_gapi_request()


if __name__ == "__main__":
    main()
    gold_price = get_gold_price()
    if gold_price:
        print(f"Current Gold Price: {gold_price}")
    else:
        print("Could not fetch gold price - please check your internet connection")

