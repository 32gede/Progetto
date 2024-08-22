import datetime
import pickle
import os
import socket
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print("Attempting to create Google Drive service...")
    print(f"Using client secret file: {client_secret_file}")
    print(f"Scopes: {scopes}")

    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print("Scopes configured:", SCOPES)

    cred = None
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        print(f"Loading credentials from {pickle_file}")
        try:
            with open(pickle_file, 'rb') as token:
                cred = pickle.load(token)
            print("Credentials loaded successfully")
        except Exception as e:
            print(f"Error loading credentials from {pickle_file}: {e}")

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            print("Refreshing credentials...")
            try:
                cred.refresh(Request())
                print("Credentials refreshed successfully")
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
        else:
            print("Generating new credentials...")
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                cred = flow.run_local_server()
                print("New credentials generated successfully")
            except Exception as e:
                print(f"Error generating new credentials: {e}")

        try:
            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)
            print(f"Credentials saved to {pickle_file}")
        except Exception as e:
            print(f"Error saving credentials to {pickle_file}: {e}")

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(f"{API_SERVICE_NAME} service created successfully")
        return service
    except Exception as e:
        print(f"Unable to connect to Google Drive API: {e}")
        return None


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt


def test_socket_connection():
    try:
        sock = socket.create_connection(("www.google.com", 80))
        print("Connection successful")
        sock.close()
    except socket.error as e:
        print(f"Socket error: {e}")
