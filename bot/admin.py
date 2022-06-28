# -*- coding: utf-8 -*-
from django.contrib import admin
from bot.models import Quote, Tag


class QuoteAdmin(admin.ModelAdmin):
    search_fields = ('text', )
    list_display = ('text', 'author', 'tag')
    autocomplete_fields = ('tag', )
    list_filter = ('tag', 'author', 'created_at')


class QuoteInline(admin.TabularInline):
    model = Quote


class TagAdmin(admin.ModelAdmin):
    search_fields = ('text',)
    inlines = [
        QuoteInline,
    ]


admin.site.register(Quote, QuoteAdmin)
admin.site.register(Tag, TagAdmin)
