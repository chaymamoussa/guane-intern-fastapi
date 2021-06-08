from subprocess import Popen


def start_celery_worker(module: str) -> Popen:
    return Popen(['celery', '-A', module, 'worker'])
