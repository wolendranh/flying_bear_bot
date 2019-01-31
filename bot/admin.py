# -*- coding: utf-8 -*-
from django.contrib import admin
from bot.models import Quote, StopWord


class QuoteAdmin(admin.ModelAdmin):
    search_fields = ('text', )
    list_display = ('text', 'author', 'stop_word')
    autocomplete_fields = ('stop_word', )
    list_filter = ('stop_word', 'author', 'text')


class QuoteInline(admin.TabularInline):
    model = Quote


class StopWordAdmin(admin.ModelAdmin):
    search_fields = ('text',)
    inlines = [
        QuoteInline,
    ]


admin.site.register(Quote, QuoteAdmin)
admin.site.register(StopWord, StopWordAdmin)
