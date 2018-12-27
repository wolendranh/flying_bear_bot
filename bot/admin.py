# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Quote, StopWord

class QuoteAdmin(admin.ModelAdmin):
    pass

class StopWordAdmin(admin.ModelAdmin):
    pass

admin.site.register(Quote, QuoteAdmin)
admin.site.register(StopWord, StopWordAdmin)
