from googleapiclient.http import MediaFileUpload
from Google import Create_Service
import os
def carica_imm(file_path, file_name):
    CLIENT_SECRET_FILE = 'credential.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    if service is not None:
        folder_id = '1Hv34hUD0h4XOi74ETwjRFkiFIuJA-RJz'
        mime_type = 'image/png' if file_name.endswith('.png') else 'image/jpeg'

        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, mimetype=mime_type)

        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        file_id = file.get('id')
        print(f'File ID: {file_id}')

        permissions = {
            'type': 'anyone',
            'role': 'reader'
        }
        service.permissions().create(
            fileId=file_id,
            body=permissions
        ).execute()

        file = service.files().get(
            fileId=file_id,
            fields='webViewLink'
        ).execute()

        shareable_link = file.get('webViewLink')
        print(f'Shareable Link: {shareable_link}')
        return file_id
    else:
        print("Failed to create the service. Please check the credentials and try again.")
        return None