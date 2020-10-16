import requests
from django.conf import settings


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TwitchClient(metaclass=Singleton):
    root_url = 'https://api.twitch.tv/helix/'
    token = None

    def __init__(self):
        self._client_secret = settings.TWITCH_CLIENT_SECRET
        self._client_id = settings.TWITCH_CLIENT_ID

        if not self.token:
            self.token = self._get_token()

    def __make_request(self, url, method):
        headers = {'Authorization': 'Bearer ' + self.token}
        return getattr(requests, method)(url=url, headers=headers)

    def _get_token(self):
        url = (f'https://id.twitch.tv/oauth2/token?client_id={self._client_id}'
               f'&client_secret={self._client_secret}&grant_type=client_credentials')
        return requests.post(url).json()['access_token']

    def games(self, game_name):
        url = f'{self.root_url}games?name={game_name}'
        return self.__make_request(url, 'get').json()

    def streams(self, game_id):
        url = f'{self.root_url}streams?game_id={game_id}'
        return self.__make_request(url, 'get').json()

    def streams_by_game(self, game_name):
        streams = None
        games = self.games(game_name=game_name)
        if games:
            game_id = games['data'][0]['id']
            streams = self.streams(game_id=game_id)
        return streams
