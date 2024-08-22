from googleapiclient.http import MediaFileUpload
from Google import Create_Service


def carica_imm(file_path, file_name):
    print(f"Starting upload for {file_name} located at {file_path}")
    CLIENT_SECRET_FILE = 'credential.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    print("Google Drive service created:", service)

    if service is not None:
        folder_id = '1Hv34hUD0h4XOi74ETwjRFkiFIuJA-RJz'
        mime_type = 'image/png' if file_name.endswith('.png') else 'image/jpeg'
        print(f"File MIME type determined: {mime_type}")

        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, mimetype=mime_type)

        try:
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            print(f"File uploaded successfully: {file}")

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
            print(f"Permissions set for file ID: {file_id}")

            file = service.files().get(
                fileId=file_id,
                fields='webViewLink'
            ).execute()
            print(f"Retrieved web view link: {file.get('webViewLink')}")
            return file_id
        except Exception as e:
            print(f"Failed to upload file: {e}")
            return None
    else:
        print("Failed to create the service. Please check the credentials and try again.")
        return None
