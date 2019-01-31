from collections import defaultdict

from django.db import IntegrityError, transaction
from django.db.models import Count
from django.core.management.base import BaseCommand
from bot.models import StopWord


class Command(BaseCommand):
    help = 'remove stop word duplicates'

    def add_arguments(self, parser):
        parser.add_argument('--dry_run', dest='dry_run', action='store_true')

    def handle(self, *args, **options):

        duplicates = StopWord.objects.values('text').annotate(Count('id')).order_by().filter(id__count__gt=1)
        duplicate_qs = StopWord.objects.filter(text__in=[d['text'] for d in duplicates])

        self.stdout.write(self.style.SUCCESS('Found {} duplicates"'.format(duplicate_qs.count())))

        counter_map = defaultdict(list)
        for stop_word in duplicate_qs:
            counter_map[stop_word.text].append(stop_word)

        if options.get('dry_run'):
            self.stdout.write(self.style.SUCCESS('Duplicates..."'))
            for text, duplicates in counter_map.items():
                self.stdout.write(self.style.SUCCESS(
                    'For text {} there are duplicates {}"'.format(text, [s.id for s in duplicates]))
                )

        duplicates_removed = 0
        quotes_moved = 0
        quotes_deleted = 0

        for text, duplicates in counter_map.items():

            original = duplicates[0]

            for duplicate in duplicates[1:]:
                quotes = duplicate.quotes.all()

                with transaction.atomic():
                    for quote in quotes:

                        self.stdout.write(self.style.SUCCESS('adding quote "{}, to keyword {}"'.format(quote.text,
                                                                                                       original.id)))
                        if not options.get('dry_run'):
                            try:
                                quote.stop_word = original
                                quote.save()
                                quotes_moved += 1
                            except IntegrityError:
                                self.stdout.write(self.style.WARNING('Removing duplicated quote "%s"'.format(
                                    quote.text)
                                ))
                                quote.delete()
                                quotes_deleted += 1

                    if not options.get('dry_run'):
                        duplicate.delete()
                        duplicates_removed += 1
                    else:
                        self.stdout.write(self.style.WARNING('Duplicated keyword {} would be removed"'.format(
                            duplicate.text)
                        ))

        self.stdout.write(self.style.SUCCESS('Duplicates removed {}, quotes moved {}, quotes deleted {}' .format(
            duplicates_removed, quotes_moved, quotes_deleted
        )))
