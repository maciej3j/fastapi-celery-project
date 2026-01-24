from celery import shared_task


@shared_task
def divide(x, y):
    import time

    time.sleep(5)
    return x / y + 2


@shared_task
def sample_task(email):
    from project.users.views import api_call

    api_call(email)
