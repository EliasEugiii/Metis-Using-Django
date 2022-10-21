from django.contrib.auth.models import User, Permission
from django.db import models
from django.utils import timezone

# Create your models here.

class Nachricht(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.CharField(max_length=400)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user} / {self.datetime}'

class Fach(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=30)
    descirption = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'
    class Meta:
        ordering = ['user', 'name', 'descirption']

class LernSet(models.Model):
    fach = models.ForeignKey(Fach, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    descirption = models.CharField(max_length=255, null=True, blank=True)
    languageOne = models.CharField(max_length=2)
    languageTwo = models.CharField(max_length=2)
    pausenzahl = models.IntegerField(default=0)
    success_points = models.IntegerField(default=0)
    richtung = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f'{self.id} / {self.name}'
    class Meta:
        ordering = ['name', 'languageOne', 'languageTwo', 'descirption']

class LernKarte(models.Model):
    lernset = models.ForeignKey(LernSet, on_delete=models.SET_NULL, null=True)
    txt_front =  models.CharField(max_length=180)
    txt_back = models.CharField(max_length=180)
    donkey_bridge = models.CharField(max_length=120, null=True, blank=True)
    success_points = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id} / {self.txt_front}'

class Progress(models.Model):
    lernkarte = models.ForeignKey(LernKarte, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    RAM_points = models.IntegerField(default=0)
    Memory_points = models.IntegerField(default=0)
    deineAntwort = models.CharField(max_length=180, null=True)
    richtigeAntwort = models.CharField(max_length=180, null=True)
    verklickt = models.BooleanField(default=False)
    datetime = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['datetime']

    def __str__(self):
        return f'{self.id} / {self.datetime}'