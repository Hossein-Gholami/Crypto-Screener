from celery import shared_task


@shared_task(name='add_nums')
def add(x,y):
    return x+y
