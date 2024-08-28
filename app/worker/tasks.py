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

@celery_app.task(
    bind=True,
    acks_late=True,
    retry_kwargs={'max_retries': 2},
)
def post_to_uri_task(
    self,
    query_uri: str = sttgs['GUANE_WORKER_URI'] + '?task_complexity=0',
    message: Dict[str, Any] = {},
    expected_status_codes: List[int] = [201, 200],
    verify: bool = True  # Add verify parameter
) -> Dict[str, Any]:
    try:
        response = post_to_uri(
            query_uri,
            message,
            expected_status_codes,
            verify
        )
        print(response.text)
        return {'status_code': response.status_code, 'data': dict(response.json())}
    except Exception as e:
        self.retry(countdown=3, exc=e)
        return {'status_code': None, 'error': str(e)}


