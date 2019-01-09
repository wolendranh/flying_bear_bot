import factory

from bot.models import Quote
from bot.tests.factories.stop_word_factory import StopWordFactory

class QuoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quote
    
    stop_word = factory.SubFactory(StopWordFactory)