from datetime import timedelta

from django.utils import timezone
from freezegun import freeze_time
import pytest

from bot.services import get_random_response_quote
from bot.tests.factories.stop_word_factory import StopWordFactory
from bot.tests.factories.quote_factory import QuoteFactory
from bot.tests.factories.quote_log_factory import QuoteLogFactory


@pytest.mark.django_db
def test_random_response_quote_no_stop_words():
    assert get_random_response_quote(message_text='max') is None

@pytest.mark.django_db
def test_random_response_quote_no_log():
    StopWordFactory(text='Arthas')
    assert get_random_response_quote(message_text='Arthas') is None

@pytest.mark.django_db
def test_random_response_quote_log_no_quote():
    stop_word = StopWordFactory(text='Arthas')

    with freeze_time(timezone.now() - timedelta(minutes=30)):
        quote = QuoteFactory(stop_word=stop_word)
        
    QuoteLogFactory(quote=quote)

    result = get_random_response_quote(message_text='Arthas')
    assert result is None

@pytest.mark.django_db
def test_random_response_quote_log_quote_found():
    stop_word = StopWordFactory(text='Arthas')
    quote = QuoteFactory(text='lagun', stop_word=stop_word)

    with freeze_time(timezone.now() - timedelta(hours=1, minutes=30)):
        hour_ago_quote = QuoteFactory(text='katka', stop_word=stop_word)
        QuoteLogFactory(quote=hour_ago_quote)

    result = get_random_response_quote(message_text='Arthas')
    assert result == quote