import random
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from .models import StopWord, Quote, QuoteLog


def store_quote(author: str, text: str, stop_word_text: str):
    stop_word, _ = StopWord.objects.get_or_create(text=stop_word_text)
    return Quote.objects.create(text=text, stop_word=stop_word, author=author)


def get_random_quote_by_stop_word(message_text: str):
    stop_word = StopWord.objects.filter(text__in=message_text.split()).first()
    if stop_word:
        quote = random.choice(stop_word.quotes.all())
        return quote
    else:
        raise StopWord.DoesNotExist


def get_random_quote():
    quote = random.choice(Quote.objects.all())
    return quote


def format_quote(quote: Quote):
    return "<i>{}</i>.\n{}".format(quote.text, quote.author or 'Unknown')

def get_random_response_quote(message_text: str):
    quote = None
    stop_word = StopWord.objects.filter(text__in=message_text.split()).first()
    if stop_word:
        latest_log = QuoteLog.objects.order_by('published_at').first()
        if latest_log and (timezone.now() - timedelta(hours=settings.RANDOM_QUOTE_INTERVAL)) > latest_log.published_at:
            quotes  = Quote.objects.filter(stop_word=stop_word).exclude(id=latest_log.quote.id)
            if quotes:
                quote = random.choice(quotes)
    return quote

def log_quote(quote: Quote):
    return QuoteLog.objects.create(quote=quote)