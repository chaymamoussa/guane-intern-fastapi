from typing import Dict, List, Any

from app.config import sttgs
from app.worker.celery_app import celery_app
from app.utils.http_request import post_to_uri
from celery.result import AsyncResult


def get_task_status(task_id: str):
    """Retrieve the status of a task by its ID."""
    result = AsyncResult(task_id, app=celery_app)
    return {
        'task_id': task_id,
        'status': result.status,
        'result': result.result,
        'date_done': result.date_done,
        'traceback': result.traceback,
    }


@celery_app.task
def post_to_uri_task(query_uri: str) -> Dict[str, Any]:
    """Task to post data to a URI and handle the response."""
    response_data = {'success': False, 'status': 'Unknown error', 'response': None}

    try:
        # Call the post_to_uri function
        response = post_to_uri(api_uri=query_uri, message={})
        if response:
            response_data['success'] = True
            response_data['status'] = 'Success'
            response_data['response'] = response.text  # Capture response text
        else:
            response_data['status'] = 'Unexpected status code or response format'
    except req.exceptions.Timeout as e:
        response_data['status'] = f'Timeout: {str(e)}'
    except Exception as e:
        response_data['status'] = f'Error: {str(e)}'

    return response_data

