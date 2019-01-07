import random
from .models import StopWord, Quote

def store_quote(author, text, stop_word_text):
    stop_word, _ = StopWord.objects.get_or_create(text=stop_word_text)
    return Quote.objects.create(text=text, stop_word=stop_word)

def get_random_quote_by_stop_word(message_text):
    return random.choice(
        StopWord.objects.filter(text__in=message_text.split()).first().quotes.all().values_list(
            'text', flat=True
            )
    )

def get_random_quote():
    return random.choice(
        Quote.objects.all().values_list(
                'text', flat=True
            )
    )