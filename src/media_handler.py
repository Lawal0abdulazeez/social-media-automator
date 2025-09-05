# Logic for downloading media
# src/media_handler.py

import os
import requests
import tempfile
import re
from typing import Optional

def _get_confirm_token(response: requests.Response) -> Optional[str]:
    """Helper function to find the confirmation token in Google's response."""
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def download_media(gdrive_url: str) -> Optional[str]:
    """
    Downloads a file from a public Google Drive link.
    
    Args:
        gdrive_url (str): The Google Drive share link (e.g., .../file/d/FILE_ID/view).

    Returns:
        Optional[str]: The local filepath to the downloaded temporary file, or None if failed.
    """
    if not gdrive_url or not isinstance(gdrive_url, str):
        print("Error: Invalid or missing Google Drive URL.")
        return None

    # Use regex to extract the file ID from various GDrive URL formats
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', gdrive_url)
    if not match:
        print(f"Error: Could not parse file ID from URL: {gdrive_url}")
        return None
    
    file_id = match.group(1)
    download_url = 'https://docs.google.com/uc?export=download'

    try:
        session = requests.Session()
        response = session.get(download_url, params={'id': file_id}, stream=True)
        
        token = _get_confirm_token(response)
        if token:
            params = {'id': file_id, 'confirm': token}
            response = session.get(download_url, params=params, stream=True)

        # Get file extension from content disposition header if available
        content_disposition = response.headers.get('content-disposition', '')
        filename_match = re.search(r'filename\*?=([^;]+)', content_disposition)
        suffix = '.tmp'
        if filename_match:
            filename = filename_match.group(1).strip().strip('"')
            # Get the extension from the original filename
            _, ext = os.path.splitext(filename)
            if ext:
                suffix = ext

        # Save the file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            for chunk in response.iter_content(chunk_size=32768):
                if chunk:
                    f.write(chunk)
            
            temp_path = f.name
            print(f"Media successfully downloaded to temporary path: {temp_path}")
            return temp_path

    except requests.exceptions.RequestException as e:
        print(f"Error downloading media from Google Drive: {e}")
        return None

def cleanup(file_path: Optional[str]):
    """
    Deletes the specified file. Used for cleaning up temporary media.
    
    Args:
        file_path (str): The path to the file to be deleted.
    """
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Cleaned up temporary file: {file_path}")
        except OSError as e:
            print(f"Error during cleanup of file {file_path}: {e}")