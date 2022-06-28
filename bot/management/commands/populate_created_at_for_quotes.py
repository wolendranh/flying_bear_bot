import json
import os
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from bot.models import Quote
from flying_bear_bot.settings import BASE_DIR


class Command(BaseCommand):

	def handle(self, *args, **options):
		with open(os.path.join(BASE_DIR, 'bot/management/commands/result.json'), 'r') as f:
			export_data = json.loads(f.read())
			text_messages_map = {m['text']: m for m in export_data['messages'] if isinstance(m['text'], str)}
			quotes = Quote.objects.all()

			quotes_to_update = []
			for quote in quotes:
				if quote.text in text_messages_map:
					export_message = text_messages_map[quote.text]
					quote.created_at = datetime.strptime(export_message['date'], "%Y-%m-%dT%H:%M:%S")
					quotes_to_update.append(quote)

			Quote.objects.bulk_update(quotes_to_update, fields=['created_at'])

		self.stdout.write(self.style.SUCCESS("Successfully updated quotes"))