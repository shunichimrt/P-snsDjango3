from django.db import models

class Category(models.Model):
    category = models.CharField("業態カテゴリ", max_length=10, blank=False)
    name     = models.CharField("業態名",      max_length=30, blank=False)

    def __str__(self):
        return str(self.name)

class Pref(models.Model):
    pref = models.CharField("都道府県ID", max_length=6, blank=False)
    name = models.CharField("都道府県名",    max_length=10, blank=False)

    def __str__(self):
        return str(self.name)
