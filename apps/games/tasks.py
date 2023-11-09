from settings.celery import app
from django.db.models import F
from django.utils import timezone
from games.models import Game, Subscribe
from celery import shared_task

@app.task
def do_test(game_id: int, *args, **kwargs):
    Game.objects.filter(id=game_id).update(
        price=F('price') + 10
    )
    print("OK")


@shared_task
def cancel_subcribe(subscribe_id):
    try:
        subscription = Subscribe.objects.get(id=subscribe_id)
        subscription.is_active = False
        subscription.datetime_finished = timezone.now()
        subscription.save()
    except Subscribe.DoesNotExist:
        pass