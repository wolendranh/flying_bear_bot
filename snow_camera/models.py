# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.postgres.fields import ArrayField


class Location(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title_en = models.CharField(max_length=200)
    title_uk = models.CharField(max_length=200, blank=True, null=True)
    url_en = models.URLField()
    url_uk = models.URLField(null=True, blank=True)
    synonyms = ArrayField(
            models.CharField(max_length=30, blank=True, null=True), default=list, null=True, blank=True
    )

    def __str__(self):
        return self.title_en


class Camera(models.Model):
    title_uk = models.CharField(max_length=200, blank=True, null=True)
    title_en = models.CharField(max_length=200)
    location = models.ForeignKey(Location, related_name="cameras", on_delete=models.CASCADE)
    url_en = models.URLField()
    url_uk = models.URLField(null=True, blank=True)
    cam_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Camera {self.title_en} for location {self.location}"
