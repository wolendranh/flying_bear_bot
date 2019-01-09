import factory

from bot.models import StopWord

class StopWordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StopWord