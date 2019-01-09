import factory

from bot.tests.factories.quote_factory import QuoteFactory
from bot.models import QuoteLog


class QuoteLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = QuoteLog
    
    quote = factory.SubFactory(QuoteFactory)