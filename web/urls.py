from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'web'
urlpatterns = [
    path('', views.index, name='index'),
    path('registrieren/', views.register_view, name='registrieren'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.settings_view, name='settings'),
    path('create-fach/', views.post_fach_view, name='create_fach'),
    path('fach/', views.fach_view, name='fach'),
    path('fach/<str:username>/<int:fachId>/sets/', views.sets_view, name='sets'),
    path('create-set/', views.post_set_view, name='create_set'),
    path('fach/<str:username>/<int:fachId>/<int:setId>/cards', views.cards_view, name='cards'),
    path('create-card/', views.post_card_view, name='create_card'),
    path('lernen/<int:setId>/<int:cardId>', views.lernen_view, name='lernen'),
    path('lernen/<int:setId>/<int:cardId>/antwort', views.antwort_view, name='antwort'),
    path('lernen/<int:setId>/<int:cardId>/create-process', views.create_process_view, name='create_process'),
    path('passwort-vergessen/', views.pw_vergessen, name='passwort_vergessen'),
    path('fortschritte/<username>', views.fortschritte_view, name='fortschritte'),
    path('chat/', views.chat_view, name='chat'),
    path('support/', views.support_view, name='support'),
    path('open-sets/', views.open_sets_view, name='open_sets'),
    path('testpersonen/', views.testpersonen_view, name='testpersonen'),
    path('SA/', views.SA_view, name='SA'),
    path('delete-card/<int:cardOwnerId>/<int:cardId>/', views.delete_card_view, name='delete-card'),
    #path('pause/', views.lernen_view, name='pause'),
    path('bearbeiten/<str:object>/<int:objectId>/', views.bearbeiten_view, name='bearbeiten'),
    path('delete-set/<int:setId>/', views.delete_set_form, name='delete-set'),
    path('delete-fach/<int:fachId>/', views.delete_fach_form, name='delete-fach'),
    path('stats-back/<int:setId>', views.stats_back_view, name='stats_back'),
]
