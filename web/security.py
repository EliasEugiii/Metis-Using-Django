
very = []
sec_warning = False
TEXT = ''
def verify_text(text):
    very = []
    sec_warning = False
    TEXT = ''
    if text == '':
        return ''
    for i in range(0, len(text)):
        if text[i] == '<':
            print('Sicherheitswarnung! Verbotenes Zeichen erkannt!')
            sec_warning = True
        elif text[i] == '>':
            print('Sicherheitswarnung! Verbotenes Zeichen erkannt!')
            print('Sicherheitswarnung: Wahrscheindlich versucht jemand Code zu injecten!')
            sec_warning = True

    if sec_warning == False:
        print('Alles in Ordnung! Keine Bedrohung festgestellt!')
        return text
    else:
        sec_warning = False
        print('Eliminierung von Bedrohung wird eingeleitet...')
        for a in range(0, len(text)):
            if text[a] == '>':
                very.append('&gt;')
            elif text[a] == '<':
                very.append('&lt;')
            else:
                very.append(text[i])
        TEXT = ''
        for b in range(0, len(text)):
            if TEXT == '':
                TEXT == very[b]
            else:
                TEXT += very[b]
        return TEXT
