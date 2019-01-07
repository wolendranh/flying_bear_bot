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
    stop_word = models.ForeignKey(StopWord, related_name='quotes', on_delete=models.CASCADE)

    def __str__ (self):
        return self.text
    
    class Meta:
        unique_together = (("text", "stop_word"),)