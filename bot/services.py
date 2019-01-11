import random
from .models import StopWord, Quote


def store_quote(author, text, stop_word_text):
    stop_word, _ = StopWord.objects.get_or_create(text=stop_word_text)
    return Quote.objects.create(text=text, stop_word=stop_word, author=author)


def get_random_quote_by_stop_word(message_text):
    stop_word = StopWord.objects.filter(text__in=message_text.split()).first()
    if stop_word:
        quote = random.choice(stop_word.quotes.all())
        return format_quote(quote=quote)
    else:
        raise StopWord.DoesNotExist


def get_random_quote():
    quote = random.choice(Quote.objects.all())
    return format_quote(quote=quote)


def format_quote(quote):
    return "<i>{}</i>.\n{}".format(quote.text, quote.author or 'Unknown')


def get_keyword_quote_count(keyword: str) -> str:
    count = Quote.objects.filter(stop_word__text=keyword).count()
    return "<i>'{}'</i> - {} quotes.".format(keyword, count)
