from django.contrib import admin
from .models import Nachricht, Fach, LernSet, LernKarte, Progress

admin.site.register(Nachricht)
admin.site.register(Fach)
admin.site.register(LernSet)
admin.site.register(LernKarte)
admin.site.register(Progress)