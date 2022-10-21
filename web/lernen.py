from django.http import HttpResponseRedirect, Http404
from .models import Nachricht, Fach, LernSet, LernKarte, Progress
from django.contrib.auth.models import Permission
import random

def getNextCard(requestUser, setId, cardId = False):
    lernSet = LernSet.objects.get(id=setId)
    cards = LernKarte.objects.filter(lernset=lernSet)

    stats = []
    stats_alle =[]
    stats_Memo0 = []
    stats_Memo1 = []
    stats_Memo2 = []
    stats_Memo3 = []
    stats_Gelernt = []
    cards = list(cards)
    if not cards:
        return False
    if lernSet.fach.user == requestUser or requestUser.is_superuser:
        for card in cards:
            stat = (Progress.objects.filter(lernkarte=card.id))
            if not stat:
                stats = stats
            else:
                stat = list(stat)
                stats.append(stat[0])

        for stat in stats:
            if stat.Memory_points == 0:
                stats_Memo0.append(stat)
                stats_alle.append(stat)
            elif stats.Memory_points == 1:
                stats_Memo1.append(stat)
                stats_alle.append(stat)
            elif stat.Memory_points == 2:
                stats_Memo2.append(stat)
                stats_alle.append(stat)
            elif stat.Memory_points == 3:
                stats_Memo3.append(stat)
                stats_alle.append(stat)
            else:
                stats_Gelernt.append(stat)


        if cardId == False:
            if stats == []:
                card = random.choice(cards)
            else:
                card = random.choice(stats_alle).lernkarte
        else:
            card = LernKarte.objects.get(id=cardId)

        # nur wenn alles möglich

        modus = random.uniform(1, 100)

        #if len(stats_Gelernt) == len(cards):
            #return 'alles gelernt'

        if stats_Memo0 != []:
            if stats_Memo1 != []:
                if stats_Memo2 != []:
                    if stats_Memo3 != []: # Memo - Mit: 0, 1, 2, 3 | Ohne:

                        if modus <= 30:
                            newCardIndex = cards.index(card) + 1
                        elif modus <= 60 and modus >= 31:
                            newCardIndex = random.choice(stats_Memo0).lernkarte
                        elif modus <= 80 and modus >= 61:
                            newCardIndex = random.choice(stats_Memo1).lernkarte
                        elif modus <= 95 and modus >= 81:
                            newCardIndex = random.choice(stats_Memo2).lernkarte
                        else:
                            newCardIndex = random.choice(stats_Memo3).lernkarte

                    else: # Memo Mit: 0, 1, 2 - Ohne: 3

                        if modus <= 30:
                            newCardIndex = cards.index(card) + 1
                        elif modus <= 60 and modus >= 31:
                            newCardIndex = random.choice(stats_Memo0).lernkarte
                        elif modus <= 85 and modus >= 61:
                            newCardIndex = random.choice(stats_Memo1).lernkarte
                        else:
                            newCardIndex = random.choice(stats_Memo2).lernkarte

                else: # Ohne Memo 2
                    if stats_Memo3 != []: # Memo Mit: 0, 1, 3 - Ohne: 2

                        if modus <= 20:
                            newCardIndex = cards.index(card) + 1
                        elif modus <= 60 and modus >= 21:
                            newCardIndex = random.choice(stats_Memo0).lernkarte
                        elif modus <= 90 and modus >= 61:
                            newCardIndex = random.choice(stats_Memo1).lernkarte
                        else:
                            newCardIndex = random.choice(stats_Memo3).lernkarte

                    else: # Memo Mit: 0, 1 - Ohne: 2, 3

                        if modus <= 30:
                            newCardIndex = cards.index(card) + 1
                        elif modus <= 80 and modus >= 31:
                            newCardIndex = random.choice(stats_Memo0).lernkarte
                        else:
                            newCardIndex = random.choice(stats_Memo1).lernkarte

            else: #ohne Memo1
                if stats_Memo2 != []:
                    if stats_Memo3 != []: # Memo Mit: 0, 2, 3 - Ohne: 1

                        if modus <= 20:
                            newCardIndex = cards.index(card) + 1
                        elif modus <= 70 and modus >= 21:
                            newCardIndex = random.choice(stats_Memo0).lernkarte
                        elif modus <= 90 and modus >= 71:
                            newCardIndex = random.choice(stats_Memo2).lernkarte
                        else:
                            newCardIndex = random.choice(stats_Memo3).lernkarte

                    else: # Memo Mit: 0, 2 - Ohne: 1, 3
                        if modus <= 10:
                            newCardIndex = cards.index(card) + 1
                        elif modus <= 70 and modus >= 11:
                            newCardIndex = random.choice(stats_Memo0).lernkarte
                        else:
                            newCardIndex = random.choice(stats_Memo2).lernkarte

                else: #ohne Memo 1, 2:
                    if stats_Memo3 != []: # Memo Mit: 0, 3  - Ohne: 1, 2

                        if modus <= 30:
                            newCardIndex = cards.index(card) + 1
                        elif modus <= 90 and modus >= 31:
                            newCardIndex = random.choice(stats_Memo0).lernkarte
                        else:
                            newCardIndex = random.choice(stats_Memo3).lernkarte

                    else: # Memo Mit: 0 - Ohne: 1, 2, 3

                        if modus <= 40:
                            newCardIndex = cards.index(card) + 1
                        else:
                            newCardIndex = random.choice(stats_Memo0).lernkarte

        else: #ohne Memo 0:
            if stats_Memo1 != []:
                if stats_Memo2 != []:
                    if stats_Memo3 != []: # Memo Mit: 1, 2, 3 - Ohne: 0

                        if modus <= 30:
                            newCardIndex = cards.index(card) + 1
                        elif modus <= 60 and modus >= 31:
                            newCardIndex = random.choice(stats_Memo1).lernkarte
                        elif modus <= 85 and modus >= 61:
                            newCardIndex = random.choice(stats_Memo2).lernkarte
                        else:
                            newCardIndex = random.choice(stats_Memo3).lernkarte

                    else: # Memo Mit: 1, 2 - Ohne: 0, 3

                        if modus <= 20:
                            newCardIndex = cards.index(card) + 1
                        elif modus <= 70 and modus >= 21:
                            newCardIndex = random.choice(stats_Memo1).lernkarte
                        else:
                            newCardIndex = random.choice(stats_Memo2).lernkarte

                else: # ohne Memo 2
                    if stats_Memo3 != []: # Memo Mit: 1, 3 - Ohne: 0, 2

                        if modus <= 30:
                            newCardIndex = cards.index(card) + 1
                        elif modus <= 80 and modus >= 31:
                            newCardIndex = random.choice(stats_Memo1).lernkarte
                        else:
                            newCardIndex = random.choice(stats_Memo3).lernkarte

                    else: # Memo Mit: 1 - Ohne: 0, 2, 3

                        if modus <= 30:
                            newCardIndex = cards.index(card) + 1
                        else:
                            newCardIndex = random.choice(stats_Memo1).lernkarte

            else: # ohne Memo 1
                if stats_Memo2 != []:
                    if stats_Memo3 != []: # Memo Mit: 2, 3 - Ohne: 0, 1

                        if modus <= 50:
                            newCardIndex = cards.index(card) + 1
                        elif modus <= 80 and modus >= 51:
                            newCardIndex = random.choice(stats_Memo2).lernkarte
                        else:
                            newCardIndex = random.choice(stats_Memo3).lernkarte

                    else: # Memo Mit: 2 - Ohne: 0, 1, 3

                        if modus <= 70:
                            newCardIndex = cards.index(card) + 1
                        else:
                            newCardIndex = random.choice(stats_Memo2).lernkarte

                else: # ohne Memo 2
                    if stats_Memo3 != []: # Memo Mit: 3 - Ohne: 0, 1, 2

                        if modus <= 70:
                            newCardIndex = cards.index(card) + 1
                        else:
                            newCardIndex = random.choice(stats_Memo3).lernkarte

                    else: # Memo Mit: Nichts - Ohne: 0, 1, 2, 3
                        newCardIndex = cards.index(card) + 1
        if isinstance(newCardIndex, int):
            if newCardIndex >= len(cards):
                newCardIndex = 0
            return cards[newCardIndex].id
        elif isinstance(newCardIndex, LernKarte):
            return newCardIndex.id
        return random.choice(cards).id

    else:
        return False


def checkAnswer(yourAnswer, setId, cardId):
    #find right answer
    richtig = None
    lernSet = LernSet.objects.get(id=setId)
    lernCard = LernKarte.objects.get(id=cardId)
    #später evt. hier noch eine if abfrage zur einstellung
    rightAnswer = lernCard.txt_back
    if rightAnswer == yourAnswer:
        richtig = True
    else:
        richtig = False
    return richtig

def createProgress(korrektheit, setId, cardId, requestUser):

    einträge = Progress.objects.filter(lernkarte=cardId)
    if not einträge:
        if korrektheit:
            return [1, 0] # RAM points = 1; Memory Points = 0
        else:
            return [0, 0] # RAM points = 0; Memory Points = 0
    else:
        letzterEintragId = einträge[len(einträge)-1].id
        letzterEintrag = Progress.objects.get(id=letzterEintragId)
        ALteRamPoints = letzterEintrag.RAM_points
        AlteMemoryPoints = letzterEintrag.Memory_points
        lastUser = letzterEintrag.user
        if requestUser == lastUser or requestUser.is_superuser:
            if korrektheit:
                if AlteMemoryPoints == 0:
                    if ALteRamPoints != 3 and ALteRamPoints < 3:
                        return [ALteRamPoints + 1, AlteMemoryPoints]
                    elif ALteRamPoints == 3 or ALteRamPoints > 3:
                        return [0, 1] # RAM points = Alte Ram pints + 1; Memory Points = 0
                else:
                    if AlteMemoryPoints != 4 and AlteMemoryPoints < 4:
                        return [0, AlteMemoryPoints + 1]
                    elif AlteMemoryPoints == 4 or AlteMemoryPoints > 4:
                        return [0, AlteMemoryPoints]

            else:
                if AlteMemoryPoints == 0:
                    if ALteRamPoints == 0 or ALteRamPoints == 1:
                        return[0, 0]
                    else:
                        return[1, 0]
                else:
                    return[ALteRamPoints, AlteMemoryPoints - 1]