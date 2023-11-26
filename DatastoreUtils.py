from datetime import datetime
import sys
from google.cloud import datastore
from google.oauth2 import service_account
from google.cloud.exceptions import GoogleCloudError, BadRequest


def to_date(date_str):
    date_time_obj = datetime.strptime(date_str, "%d %b %Y")
    return date_time_obj


def currency_to_integer(currency_string):
    cleaned_string = currency_string.replace("Rp ", "").replace(".", "")
    currency_integer = int(cleaned_string)
    return currency_integer


def initialize_datastore_client(credentials_file):
    try:
        datastore_client = datastore.Client(
            credentials=service_account.Credentials.from_service_account_file(
                credentials_file
            )
        )
        return datastore_client
    except GoogleCloudError as gce:
        print(f"A Google Cloud error occurred: {gce}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
        


def put_entity(client, entity):
    try:
        client.put(entity)
    except BadRequest as bre:
        print(
            f"A bad request error occurred: {bre} Entity won't be added to the database"
        )
    except GoogleCloudError as gce:
        print(
            f"A Google Cloud error occurred: {gce} Entity won't be added to the database"
        )


def create_entity(client, kind):
    try:
        key = client.key(kind)
        entity = datastore.Entity(key=key)
        return entity
    except BadRequest as bre:
        print(
            f"A bad request error occurred: {bre} Entity won't be added to the database"
        )
    except GoogleCloudError as gce:
        print(
            f"A Google Cloud error occurred: {gce} Entity won't be added to the database"
        )
