import os
from shutil import copyfileobj
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from shutil import copyfileobj

import requests as req

from app.config import sttgs


req_timeout = int(sttgs.get('REQUESTS_TIMEOUT', 20))


def get_dog_picture(
    api_uri: Optional[str] = sttgs.get('DOG_API_URI')
) -> Optional[str]:
    """Returns None if an exception occurs.
    """
    if api_uri:

        try:
            r = req.get(api_uri, timeout=req_timeout)
        except req.exceptions.Timeout:
            return time_out_message(api_uri, req_timeout)
        except Exception:
            return None

        data_json = r.json()

        if (not r.status_code == 200) or (not isinstance(data_json, dict)):
            return None

        if data_json.get('status') == 'success':
            return data_json.get('message')

    return None


def post_file_to_uri(
    upload_file_path: Path,
    uri: str = sttgs.get('UPLOAD_FILE_URI'),
    file_content: str = 'image/png',
    *,
    message: str,
    verify: bool = True  # Add verify parameter here
) -> Union[req.Response, str]:
    """Post a file to uri."""
    # if file does not exist, post a text file
    os.makedirs(upload_file_path.parent, exist_ok=True)
    if not os.path.isfile(upload_file_path):
        upload_file_path = upload_file_path.parent / 'hello_guane.txt'
        file_content = 'text/plain'
        message = 'Original file was replaced by api.'
        with open(upload_file_path, 'w') as save_file:
            print("hereeeeee")
            save_file.write('Hello chayma!')

    # Read file and upload it to uri it using requests library
    with open(upload_file_path, 'rb') as payload:
        files_to_upload = {
            'file': (
                upload_file_path.name,
                payload,
                file_content
            )
        }
        try:
            request = req.post(
                uri,
                files=files_to_upload,
                data={'message': message},
                verify=verify # Disable SSL verification
            )
        except req.exceptions.Timeout:
            return time_out_message(uri, req_timeout)

        # Log response content for debugging
        print("Response Content:", request.text)
        print(f"Response Status Code: {request.status_code}")
        print(f"Response Content-Type: {request.headers.get('Content-Type')}")
        print(f"Response Content: {request.text}")

        if request.status_code == 500:
            print("Server error: Internal Server Error (500)")
            print("Response content:", request.text)  # Print response content for debugging
            return None

        # Save a copy of the file just to verify that the uploaded object was
        # correctly read
        save_file_copy_path = (
            upload_file_path.parent / ('2-' + upload_file_path.name)
        )
        with open(save_file_copy_path, 'wb') as save_file_copy:
            payload.seek(0)
            copyfileobj(payload, save_file_copy)
    return request


def post_to_uri(
    api_uri: str,
    message: Dict[str, Any],
    expected_status_codes: List[int] = [200, 201]
) -> Optional[req.Response]:
    try:
        response = req.post(api_uri, data=message, timeout=req_timeout)
    except req.exceptions.Timeout:
        raise req.exceptions.Timeout(time_out_message(api_uri, req_timeout))

    # Log response content for debugging
    print("Response Content:", response.text)
    data_json = response.json()

    status_code_is_not_expected = (
        response.status_code not in expected_status_codes
    )

    if status_code_is_not_expected or (not isinstance(data_json, dict)):
        return None

    return response


def time_out_message(server, secs: int):
    return f'The request to {server} timed out after {secs} seconds.'


example_dog_urls = [
    "https://images.dog.ceo/breeds/retriever-golden/nina.jpg",
    "https://images.dog.ceo/breeds/papillon/n02086910_1613.jpg",
    "https://images.dog.ceo/breeds/buhund-norwegian/hakon1.jpg",
    "https://images.dog.ceo/breeds/terrier-toy/n02087046_4409.jpg",
]
