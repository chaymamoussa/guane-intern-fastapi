from pathlib import Path
from typing import Any
import base64
import json

from fastapi import APIRouter, Request, Depends, HTTPException, status
import requests as req

from app import schemas
from app.config import sttgs
from app.crud import superuser_crud
from app.utils.http_request import post_file_to_uri
from app.utils.paths import join_relative_path




upload_file_router = APIRouter()


@upload_file_router.post(
    '/file-to-guane',
    response_model=schemas.UploadFileStatus,
    status_code=status.HTTP_201_CREATED,
)
async def post_file_to_guane(
    client_req: Request,
    current_superuser: schemas.SuperUser = Depends(
        superuser_crud.get_current_active_user
    )
) -> Any:
    """With an empty body request to this endpoint, the API sends a locally
    stored file to a previously defined endpoint (in this case, Guane's test
    API).
    """
    this_file_path = Path(__file__).parent.absolute()
    print("#########################")
    print(this_file_path)
    upload_file_path = join_relative_path(
        this_file_path,
        sttgs.get('UPLOAD_FILE_PATH')
    )
    print("#########################")
    print(upload_file_path)

    upload_req = post_file_to_uri(
        upload_file_path,
        message='Hello chayma!',
        verify=False  # Disable SSL verification for testing purposes
    )
    print("################################")
    print(upload_req)

    # If timeout in upload_request or request fails
    if not isinstance(upload_req, req.Response):
        if upload_req:
            raise HTTPException(
                status_code=502,
                detail={
                    'success': False,
                    'remote_server_response': None,
                    'remote_server_status_code': None,
                    'message': upload_req
                }
            )
        else:
            raise HTTPException(status_code=502)

    # Try to extract JSON data from the response
    try:
        remote_server_response = upload_req.json()
    except ValueError:  # In case response is not JSON
        remote_server_response = upload_req.text  # Fallback to plain text response
    # Extract and decode the file content if available
    file_content = None
    if 'files' in remote_server_response and 'hello_guane.txt' in remote_server_response['files']:
        base64_data = remote_server_response['files']['hello_guane.txt']
        # Remove data URL prefix if present
        base64_data = base64_data.split(",")[-1]
        file_content = base64.b64decode(base64_data).decode('utf-8')
        print("File content:")
        print(file_content)
    return {
        'success': upload_req.status_code == 200,
        'remote_server_response': remote_server_response,
        'remote_server_status_code': upload_req.status_code
    }

