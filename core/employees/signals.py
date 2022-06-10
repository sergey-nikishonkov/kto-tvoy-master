from datetime import time
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Schedule, Hours


HOURS = ('10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30','16:00', '16:30','17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00')

@receiver(post_save, sender=Schedule)
def add_working_hours(sender, **kwargs):
    print()
    if kwargs['created']:
        for hour in HOURS:
            Hours.objects.create(schedule=kwargs['instance'], hour=time.fromisoformat(hour))



