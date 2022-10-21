import django.core.exceptions
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.forms import UserCreationForm, AuthenticationForm --> veraltet brauchen wir nicht mehr (standart login form)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .lernen import getNextCard, checkAnswer, createProgress
from .security import verify_text

from .models import Fach, LernSet, LernKarte, Progress
from .forms import RegisterForm, LoginForm, FachForm, SetForm, CardForm
from Metis.settings import BASE_DIR

from django.views.decorators.csrf import csrf_exempt




# Create your views here.

original_link = 'https://web-production-7657.up.railway.app/'

@login_required #-->mann kann die Seite nur betreten, wenn man eingolggt ist, ansosten wird man auf login weitergeleitet
def index(request):
    return render(request, 'web/base.html')

@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('web:index'))
    login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = verify_text(login_form.cleaned_data['username'])
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('web:index'))
    return render(request, 'web/login.html', {'login_form': login_form})

@csrf_exempt
@login_required
def fortschritte_view(request, username):
    user = get_object_or_404(User, username=username)
    if username == request.user.username or request.user.is_superuser:
        return render(request, 'web/fortschritte.html', {'user': user})
    else:
        raise Http404('Du hast keinen Zugriff auf diese Stats, bitte wende dich bei Fragen an den Administrator')

@csrf_exempt
@login_required
def SA_view(request):
    return render(request, 'web/SA.html')

@csrf_exempt
@login_required
def open_sets_view(request):
    return render(request, 'web/open-sets.html')

@csrf_exempt
@login_required
def chat_view(request):
    return render(request, 'web/chat.html')

@csrf_exempt
@login_required
def testpersonen_view(request):
    return render(request, 'web/testpersonen.html')

@csrf_exempt
def support_view(request):
    return render(request, 'web/support.html')

@csrf_exempt
def pw_vergessen(request):
    return render(request, 'web/passwort-vergessen.html')

@csrf_exempt
def register_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('web:index'))
    register_form = RegisterForm()
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = verify_text(register_form.cleaned_data['username'])
            password = register_form.cleaned_data['password']
            email = verify_text(register_form.cleaned_data['email'])
            first_name = verify_text(request.POST['first_name'])
            last_name = verify_text(request.POST['last_name'])
            User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('web:index'))
    return render(request, 'web/register.html', {'register_form': register_form})

@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect(reverse('web:index'))

@csrf_exempt
@login_required
def settings_view(request):
    return render(request, 'web/settings.html')

@csrf_exempt
@login_required
def post_fach_view(request):
    fach_form = FachForm(request.POST)
    if fach_form.is_valid():
        fach = fach_form.save(commit=False)
        fach.user = request.user
        fach.name = verify_text(fach.name)
        fach.descirption = verify_text(fach.descirption)
        fach.save()
    return HttpResponseRedirect(reverse('web:fach'))

@csrf_exempt
@login_required
def fach_view(request):
    html_fach = ''
    fach_form = FachForm(request.POST)
    fach_user = Fach.user
    faecher = Fach.objects.all().order_by('user')
    faecher_user = Fach.objects.filter(user=request.user)

    if request.user.is_superuser:
        for post in faecher:
            html_fach += f"""
            <tr class='clickable-row' data-href='{original_link}fach/{request.user}/{post.id}/sets'>
                <th scope="row"></th>
                <td>{post.user}</td>
                <td>{post.name}</td>
                <td>{post.descirption}</td>
                <td></td>

            </tr>
            """
    else:
        for post in faecher_user:
            html_fach += f"""
                <tr class='clickable-row' data-href='{original_link}fach/{request.user}/{post.id}/sets'>
                    <th scope="row"></th>
                    <td>{post.name}</td>
                    <td>{post.descirption}</td>
                    <td></td>
            </tr>
            """
    return render(request, 'web/fach.html', {'facher': faecher, 'faecher_user': faecher_user, 'fach_form': fach_form, 'fach_user': fach_user, 'html_fach': html_fach})

@csrf_exempt
@login_required
def post_set_view(request):
    set_form = SetForm(request.POST)
    set = set_form.save(commit=False)
    if set_form.is_valid():
        set.user = request.user
        set.fach = Fach.objects.get(id=request.POST['fach'])
        set.languageOne = request.POST['btnradio_lang1']
        set.languageTwo = request.POST['btnradio_lang2']
        set.save()
    return HttpResponseRedirect(reverse('web:sets', kwargs={'username': request.user.username, 'fachId': set.fach.id}))

@csrf_exempt
@login_required
def stats_back_view(request, setId):
    set = get_object_or_404(LernSet, id=setId)
    cards = LernKarte.objects.filter(lernset=set.id)
    if set.fach.user == request.user or request.user.is_superuser:
        for card in cards:
            stat = Progress(lernkarte=card, user=set.fach.user, RAM_points=0, Memory_points=0, deineAntwort='Zurückgesetzte Stats', richtigeAntwort='Zurückgesetzte Stats')
            stat.save()
            card.success_points = 0
            card.save()
        return HttpResponseRedirect(reverse('web:cards', kwargs={'username': set.fach.user.username, 'fachId': set.fach.id, 'setId': setId}))
    else:
        raise Http404('Du hast keine Berrechtigung diese Stats zu ändern! Bei Fragen wende dich bitte an den Admin.')

@csrf_exempt
@login_required
def delete_card_view(request, cardOwnerId, cardId):
    card = get_object_or_404(LernKarte, id=cardId)
    owner = get_object_or_404(User, id=cardOwnerId)
    fach = Fach.objects.get(id=card.lernset.fach.id)
    set = LernSet.objects.get(id=card.lernset.id)
    if owner.id == request.user.id or request.user.is_superuser:
        card.delete()
        return HttpResponseRedirect(reverse('web:cards', kwargs={'username': owner.username, 'fachId': fach.id, 'setId': set.id}))
    else:
        raise Http404('Du hast keine Berrechtigung diese Karte zu löschen. Wende dich bei Fragen an den Admin')

@csrf_exempt
@login_required
def sets_view(request, username, fachId):
    user = get_object_or_404(User, username=username)
    fach = get_object_or_404(Fach, id=fachId)
    set_form = SetForm(request.POST)
    html_sets = ''
    sets = LernSet.objects.filter(fach=fach).order_by('name')
    if user == request.user or request.user.is_superuser:
        for post in sets:
            html_sets += f"""
            <tr class='clickable-row' data-href='{original_link}fach/{request.user}/{post.fach.id}/{post.id}/cards'>
                <td></td>
                <td>{post.name}</td>
                <td>{post.languageOne}</td>
                <td>{post.languageTwo}</td>
                <td>{post.descirption}</td>
            </tr>
            """
        return render(request, 'web/sets.html', {'html_sets': html_sets, 'user': user, 'fach': fach, 'set_form': set_form,})
    else:
        return HttpResponseRedirect(reverse('web:fach'))

@csrf_exempt
@login_required
def cards_view(request, username, fachId, setId):
    user = get_object_or_404(User, username=username)
    fach = get_object_or_404(Fach, id=fachId)
    set = get_object_or_404(LernSet, id=setId)
    next_card_id = getNextCard(request.user, setId)
    card_form = CardForm(request.POST)
    cards = LernKarte.objects.filter(lernset=set)
    fortschritte = []
    if user == request.user or request.user.is_superuser:
        return render(request, 'web/cards.html', {'setId': setId, 'user': user, 'fach': fach, 'card_form': card_form, 'set': set, 'cards': cards, 'next_card_id': next_card_id})
    else:
        raise Http404('Fehlende Berrechtigung: Du hast kein Zugriffsrecht auf den Inhalt dieses Lernsets. Bei Fragen kannst du dich gerne an den Admin wenden.')

@login_required
@csrf_exempt
def post_card_view(request):
    card_form = CardForm(request.POST)
    lernset = LernSet.objects.get(id=request.POST['lernset'])
    card = card_form.save(commit=False)
    if card_form.is_valid():
        card.lernset = lernset
        card.save()
    return HttpResponseRedirect(reverse('web:cards', kwargs={'username': request.user.username, 'fachId': lernset.fach.id, 'setId': lernset.id}))

@login_required
@csrf_exempt
def delete_set_form(request, setId):
    set = get_object_or_404(LernSet, id=setId)
    owner = set.fach.user
    if owner == request.user or request.user.is_superuser:
        set.delete()
        return HttpResponseRedirect(reverse('web:fach'))
    else:
        raise Http404('Du hast keine Berrechtigung dieses Lernset zu löschen. Wende dich bei Fragen an den Admin')

@login_required
@csrf_exempt
def delete_fach_form(request, fachId):
    fach = get_object_or_404(Fach, id=fachId)
    owner = fach.user
    if owner == request.user or request.user.is_superuser:
        fach.delete()
        return HttpResponseRedirect(reverse('web:fach'))
    else:
        raise Http404('Du hast keine Berrechtigung dieses Fach zu löschen. Wende dich bei Fragen an den Admin')

@login_required
@csrf_exempt
def bearbeiten_view(request, object, objectId):
    if object == 'set':
        set = get_object_or_404(LernSet, id=objectId)
        object = 'set'
        if set.fach.user == request.user or request.user.is_superuser:
            return render(request, 'web/bearbeiten.html', {'set': set, 'object': object})
        else:
            raise Http404('du hast leidere keinen Zugriff auf gefordetes Objekt: wenden sie sich bei Fragen an den Admin')
    elif object == 'fach':
        fach = get_object_or_404(Fach, id=objectId)
        object = 'fach'
        if fach.user == request.user or request.user.is_superuser:
            return render(request, 'web/bearbeiten.html', {'fach': fach, 'object': object})
        else:
            raise Http404('du hast leidere keinen Zugriff auf gefordetes Objekt: wenden sie sich bei Fragen an den Admin')
    else:
        raise Http404('Fehler 303: Objectname falsch; wenden sie sich bei Fragen an den Admin')


    #später das hier verwenden
    if object == 'card':
        card = get_object_or_404(LernKarte, id=objectId)
        object = 'card'
        if card.lernset.fach.user == request.user or request.user.is_superuser:
            return render(request, 'web/bearbeiten.html', {'card': card, 'object':object})
        else:
            raise Http404('du hast leidere keinen Zugriff auf gefordetes Objekt: wenden sie sich bei Fragen an den Admin')

    elif object == 'set':
        set = get_object_or_404(LernSet, id=objectId)
        object = 'set'
        if set.fach.user == request.user or request.user.is_superuser:
            return render(request, 'web/bearbeiten.html', {'set': set, 'object': object})
        else:
            raise Http404('du hast leidere keinen Zugriff auf gefordetes Objekt: wenden sie sich bei Fragen an den Admin')

    elif object == 'fach':
        fach = get_object_or_404(Fach, id=objectId)
        object = 'fach'
        if fach.user == request.user or request.user.is_superuser:
            return render(request, 'web/bearbeiten.html', {'fach': fach, 'object': object})
        else:
            raise Http404('du hast leidere keinen Zugriff auf gefordetes Objekt: wenden sie sich bei Fragen an den Admin')

    else:
        raise Http404('Fehler 303: Objectname falsch; wenden sie sich bei Fragen an den Admin')

@login_required
@csrf_exempt
def lernen_view(request, setId, cardId):
    set = get_object_or_404(LernSet, id=setId)
    card = get_object_or_404(LernKarte, id=cardId)
    #set.pausenzahl += 1
    set.save()
    html_stats = ''
    if False:#set.pausenzahl >= 25:
        set.pausenzahl = 0
        set.save()
        states = Progress.objects.filter(user=request.user)
        stats = []
        for i in range(len(states) - 1, 0, -1):
            stats.append(states[i].id)
        for stat in stats:
            stat = Progress.objects.get(id=stat)
        states = stats
        stats = []
        for i in range(0, 24):
            stats.append(states[i])

        for INDEX, stat in enumerate(stats):
            stat = Progress.objects.get(id=stat)
            PROGRESS = 0
            PROGRESS_VORHER = 0
            DIFFERENZ = 0
            RAM = stat.RAM_points
            if not RAM:
                RAM = 0

            MEMORY = stat.Memory_points
            if not MEMORY:
                MEMORY = 0

            yourAnswer = stat.deineAntwort
            if not yourAnswer:
                yourAnswer=''

            correctAnswer = stat.richtigeAntwort
            if not correctAnswer:
                correctAnswer=''

            verklickt = stat.verklickt
            if not verklickt:
                verklickt=False

            richtigkeit = False
            if yourAnswer == correctAnswer or verklickt == True:
                richtigkeit = True
            else:
                richtigkeit = False

            if MEMORY == 0:
                PROGRESS = RAM * 15
            else:
                if MEMORY != 4:
                    PROGRESS = MEMORY * 15
                    PROGRESS += 45
                else:
                    PROGRESS = 100

            karte = LernKarte.objects.get(id=stat.lernkarte.id)
            fortschritte = Progress.objects.filter(lernkarte=karte)
            fortschritt_index = len(fortschritte)
            fortschritt_index += -2
            fortschritte_indexe = []
            for i in range(fortschritt_index, 0, -1):
                fortschritte_indexe.append(fortschritte[i])
            fortschritte_indexe = fortschritte_indexe[0]
            fortschritt_index = fortschritte_indexe[0]
            fortschritt_id = fortschritte[fortschritt_index].id
            fortschritt_objekt = Progress.objects.get(id=fortschritt_id)
            RAM_VORHER = fortschritt_objekt.RAM_points
            MEMORY_VORHER = fortschritt_objekt.Memory_points

            if MEMORY_VORHER == 0:
                PROGRESS_VORHER = RAM_VORHER * 15
            else:
                if MEMORY_VORHER != 4:
                    PROGRESS_VORHER = MEMORY_VORHER * 15
                    PROGRESS_VORHER += 45
                else:
                    PROGRESS_VORHER = 100

            if verklickt == True:
                verklickt = '🟢'
            else:
                verklickt = '🔴'

            DateTime = stat.datetime
            DateTime = DateTime.strftime("%d/%m/%y %H:%M:%S")

            if richtigkeit:
                DIFFERENZ = PROGRESS - PROGRESS_VORHER

                html_stats += f"""
                    <tr>
                        <td><p style="color:white">{INDEX}.</p></td>
                        <td><p style="color:green"></p></td>
                        <td>🟢</td>
                            <div class="progress bg-dark border border-success" style="margin-top:0.75rem">
                                <div class="progress-bar bg-success" role="progressbar" style="width:{PROGRESS_VORHER}%; display:inline" aria-valuenow="{PROGRESS_VORHER}" aria-valuemin="0" aria-valuemax="100"> <h9 style="font-weight: bold; text-align: left;">{PROGRESS}%</h9></div>
                                <div class="progress-bar progress-bar-striped progress-bar-animated bg-success" role="progressbar" aria-valuenow="{DIFFERENZ}" aria-valuemin="0" aria-valuemax="100" style="width: {DIFFERENZ}%"></div>
                            </div>
                        </td>
                        <td><p style="color:green">+ {DIFFERENZ}%</p></td>
                        <td><p style="color:green">{yourAnswer}</p></td>
                        <td><p style="color:green">{correctAnswer}</p></td>
                        <td><p style="color:green">{verklickt}</p></td>
                        <td><p style="color:white">{DateTime} Uhr</p></td>
                    </tr>
                    """
            else:
                DIFFERENZ = PROGRESS_VORHER - PROGRESS
                html_stats += f"""
                    <tr>
                        <td><p style="color:white">{INDEX}.</p></td>
                        <td><p style="color:red"></p></td>
                        <td>🔴</td>
                            <div class="progress bg-dark border border-success" style="margin-top:0.75rem">
                                <div class="progress-bar bg-success" role="progressbar" style="width:{PROGRESS}%; display:inline" aria-valuenow="{PROGRESS}" aria-valuemin="0" aria-valuemax="100"> <h9 style="font-weight: bold; text-align: left;">{PROGRESS}%</h9></div>
                                <div class="progress-bar progress-bar-striped progress-bar-animated bg-danger" role="progressbar" aria-valuenow="{DIFFERENZ}" aria-valuemin="0" aria-valuemax="100" style="width: {DIFFERENZ}%"></div>
                            </div>
                        </td>
                        <td><p style="color:red">- {DIFFERENZ}%</p></td>
                        <td><p style="color:red">{yourAnswer}</p></td>
                        <td><p style="color:red">{correctAnswer}</p></td>
                        <td><p style="color:red">{verklickt}</p></td>
                        <td><p style="color:white">{DateTime} Uhr</p></td>
                    </tr>
                    """
        return render(request, 'web/pause.html', {'setId': setId, 'cardId': cardId, 'stats': stats, 'html_stats': html_stats})

    if set.fach.user == request.user or request.user.is_superuser:
        return render(request, 'web/lernen.html', {'card': card, 'setId': setId, 'cardId': cardId})
    raise Http404('Das Lernset wurde nicht gefunden (wende dich bei Fragen an den Admin (Elias))')


@login_required
@csrf_exempt
def antwort_view(request, setId, cardId):
    set = get_object_or_404(LernSet, id=setId)
    card = get_object_or_404(LernKarte, id=cardId)
    your_antwort = request.POST['antwort']
    richtig = checkAnswer(your_antwort, setId, cardId)
    return render(request, 'web/answer.html', {'card': card, 'setId': setId, 'cardId': cardId, 'your_antwort': your_antwort, 'richtig': richtig})

@login_required
@csrf_exempt
def create_process_view(request, setId, cardId):
    set = get_object_or_404(LernSet, id=setId)
    card = get_object_or_404(LernKarte, id=cardId)
    korrektheit = request.POST['korrektheit']
    yourAnswer = request.POST['yourAnswer']
    correctAnswer = request.POST['correctAnswer']
    try:
        verklickt = request.POST['verklickt_checkbox']
        verklick = 'on'
    except:
        verklickt = 'off'

    if verklickt == 'on':
        korrektheit = True

    if verklickt == 'off':
        verklickt = False
    else:
        verklickt = True

    data = createProgress(korrektheit, setId, cardId, request.user)
    RAM = data[0]
    MEMORY = data[1]
    PROGRESS = 0
    if MEMORY == 0:
        PROGRESS = RAM * 15
    else:
        if MEMORY != 4:
            PROGRESS = MEMORY * 15
            PROGRESS += 45
        else:
            PROGRESS = 100

    card.success_points = PROGRESS
    card.save()
    p = Progress(lernkarte=card, user=request.user, RAM_points=RAM, Memory_points=MEMORY, deineAntwort=yourAnswer, richtigeAntwort=correctAnswer, verklickt=verklickt)
    p.save()

    neueKarteId = getNextCard(request.user, setId, cardId)

    return HttpResponseRedirect(reverse('web:lernen', kwargs={'setId': setId, 'cardId': neueKarteId}))
