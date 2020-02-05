import html
import random
import requests

from twitch.client import TwitchClient
from .models import Tag, Quote


def store_quote(author: str, text: str, tag_text: str):
    tag, _ = Tag.objects.get_or_create(text=tag_text)
    return Quote.objects.create(text=text, tag=tag, author=author)


def get_random_quote_by_tag(message_text: str) -> str:
    tag = Tag.objects.filter(text__in=message_text.split()).first()
    if tag:
        quote = random.choice(tag.quotes.all())
        return format_quote(quote=quote)
    else:
        raise Tag.DoesNotExist


def get_random_quote() -> str:
def get_weather(city):
    response = requests.get('http://wttr.in/{0}?format=4'.format(city))
    return response.text


def get_random_quote():
    quote = random.choice(Quote.objects.all())
    return format_quote(quote=quote)


def format_quote(quote: Quote) -> str:
    return "<i>{}</i>\n{}".format(quote.text, quote.author or 'Unknown')


def get_keyword_quote_count(keyword: str) -> str:
    count = Quote.objects.filter(tag__text=keyword).count()
    return "<i>'{}'</i> - {} quotes.".format(keyword, count)


def format_stream(idx, stream):
    return (
        f'<b>- {idx} -</b> \n'
        f'<i>{html.escape(stream["title"])}</i>\n'
        f'\n'
        f'<b>streamer:</b> <i>{html.escape(stream["user_name"])}</i>\n'
        f'\n'
        f'<b>viewers:</b> <i>{stream["viewer_count"]}</i>\n'
        f'<a href="https://www.twitch.tv/{html.escape(stream["user_name"])}">Stream link</a>\n'
        f'\n'
        f'\n'
    )


def get_stream_list_by_game(game_name: str):
    client = TwitchClient()

    streams = client.streams_by_game(game_name=game_name)
    raw_streams = streams['data']

    # limit to 5 for now
    if len(raw_streams) >= 5:
        raw_streams = raw_streams[:5]

    parsed_streams = []
    for idx, stream in enumerate(raw_streams):
        parsed_streams.append(format_stream(idx, stream))

    return ' '.join(parsed_streams)
