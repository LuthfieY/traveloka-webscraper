from datetime import datetime
from google.cloud import datastore
from google.oauth2 import service_account

def to_date(date_str):
    date_time_obj = datetime.strptime(date_str, "%d %b %Y")
    return date_time_obj


def currency_to_integer(currency_string):
    cleaned_string = currency_string.replace("Rp ", "").replace(".", "")
    currency_integer = int(cleaned_string)
    return currency_integer


def initialize_datastore_client(credentials_file):
    return datastore.Client(
        credentials=service_account.Credentials.from_service_account_file(
            credentials_file
        )
    )