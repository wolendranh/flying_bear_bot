# -*- coding: utf-8 -*-
from django.db import models


class StopWord(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=200)

    def __str__ (self):
        return self.text


class Quote(models.Model):
    text = models.CharField(max_length=400)
    author = models.CharField(blank=True, null=True, max_length=100)
    stop_word = models.ForeignKey(StopWord, related_name='quotes', on_delete=models.CASCADE)

    def __str__ (self):
        return self.text
    
    class Meta:
        unique_together = (("text", "stop_word"),)

class QuoteLog(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='logs')
    published_at = models.DateTimeField(auto_now_add=True)
    quote_of_the_day_at = models.DateTimeField(null=True, blank=True)
