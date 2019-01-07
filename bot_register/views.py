import json
import logging
from collections import defaultdict

from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponse
from django.http.response import Http404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.module_loading import import_string
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from telegram import Bot, Update
from telegram.ext import Dispatcher

logger = logging.getLogger(__name__)



@method_decorator(csrf_exempt, name='dispatch')
class TelegramView(generic.View):
    bots = defaultdict()

    @classmethod
    def register_webhooks(cls):

        for bot_config in settings.TELEGRAM_BOT:
            bot = Bot(bot_config['token'])

            if 'webhook' in bot_config:
                url = bot_config['webhook'] % bot.token
                if url[-1] != '/':
                    url += '/'
            else:
                webhook = reverse('bot_hook', kwargs={'token': bot.token})
                from django.contrib.sites.models import Site
                current_site = Site.objects.get_current()
                url = 'https://' + current_site.domain + webhook

            bot.set_webhook(url)
            bot = Bot(bot_config['token'])
            dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)
            register = import_string(bot_config['register'])

            register(dispatcher)

            cls.bots[bot.token] = dispatcher

            logger.info('bot %s registered on url %s', bot.token, url)

    @classmethod
    def as_view(cls, **initkwargs):
        cls.register_webhooks()
        return super().as_view(**initkwargs)

    def get(self, request):
        return HttpResponse()

    def head(self, request):
        return HttpResponse()

    def post(self, request, token, *args,):
        dispatcher = self.get_dispatcher(token)
        if not dispatcher:
            return Http404()

        json_string = request.body.decode('utf-8')
        update = Update.de_json(data=json.loads(json_string), bot=dispatcher.bot)
        dispatcher.process_update(update)
        return HttpResponse()

    @classmethod
    def get_dispatcher(cls, token):
        dispatcher = None
        if token in cls.bots:
            return cls.bots[token]
        return dispatcher
