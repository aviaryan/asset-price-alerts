import os
from dotenv import load_dotenv
# own libraries
from lib.providers import make_gapi_request
from lib.notify import show_notification

load_dotenv()

def main():
    gold_price = get_gold_price()
    print('Gold price: ', gold_price)
    show_notification('Gold Price is $' + str(gold_price), 'Asset Alert', 'Your alert is triggered')


def get_gold_price():
    try:
        return make_gapi_request(os.getenv("GOLDAPI_IO_API_KEY"))
    except Exception as e:
        print(f"Error fetching gold price. This should not happen: {e}")
        return None

if __name__ == "__main__":
    main()
