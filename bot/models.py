# -*- coding: utf-8 -*-
from django.db import models


class Tag(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Quote(models.Model):
    text = models.CharField(max_length=400)
    author = models.CharField(blank=True, null=True, max_length=100)
    tag = models.ForeignKey(Tag, related_name='quotes', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.text
    
    class Meta:
        unique_together = (("text", "tag"),)
