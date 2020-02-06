import html
import random
import requests

from django.conf import settings
from twitch.client import TwitchClient
from .models import Tag, Quote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait

location = "Drahobrat"


def get_location_snow_camera_screenshot(location: str):
    options = webdriver.ChromeOptions()
    options.binary_location = settings.GOOGLE_CHROME_BIN
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    options.headless = True

    driver = webdriver.Chrome(executable_path=settings.CHROMEDRIVER_PATH, options=options)
    driver.get("https://snig.info/uk")

    elem = driver.find_elements_by_xpath("//a[contains(@href, '/uk/{0}') and contains(@class, 'card--object')]".format(location))[0]
    elem.click()

    videos = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href, '/uk/{}') and contains(@class, 'card--object')]".format(location))))

    videos.click()

    videos = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".fp-ui")))
    player = driver.find_element_by_class_name('fp-ui')
    player.click()
    active_video = WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element(
        (By.XPATH, "//span[contains(@class, 'fp-elapsed')]"), "00:01")
    )
    screenshot_location = player.screenshot("/tmp/{}.png".format(location))
    driver.close()
    return screenshot_location


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
