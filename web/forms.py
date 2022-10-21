from django import forms
from django.contrib.auth.models import User
from .models import Nachricht, Fach, LernSet, LernKarte, Progress

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, label='Username', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'style': 'width: 100%;float:left;',
            'placeholder': 'Dein Username'
                }
    ))
    password = forms.CharField(min_length=6, max_length=50, label='Passwort', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'style': 'width: 100%;float:left;',
            'placeholder': 'Dein Passwort'
                }
    ))

    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'style': 'width: 100%;float:left;',
            'placeholder': 'Deine Email'
                }
    ))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Dieser Username existiert bereits!')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Diese Email existiert bereits!')
        return email

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='Username', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'style': 'width: 100%;float:left;',
            'placeholder': 'Dein Username'
                }
    ))

    password = forms.CharField(min_length=6, max_length=50, label='Passwort', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'style': 'width: 100%;float:left;',
            'placeholder': 'Dein Passwort'
                }
    ))

class FachForm(forms.ModelForm):
    name = forms.CharField(label='', empty_value='hi', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'style': 'width: 100%;float:left; margin-right: 1rem;',
            'placeholder': 'Fachname: z.B. Englisch',
            'maxlength': '30',
        }
    ))
    descirption = forms.CharField(required=False, label='', empty_value='', widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'style': 'width: 100%;float:left;resize: none; margin-top:1rem',
            'placeholder': 'Beschreibung: z.B. Mein Wortschatz im Englisch in der FMS',
            'maxlength': '255',
        }
    ))
    class Meta:
        model = Fach
        fields =['name', 'descirption']

class SetForm(forms.ModelForm):
    name = forms.CharField(label='', empty_value='Hallo', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'style': 'width: 100%;float:left; margin-top:1rem;',
            'placeholder': 'Lernset-Name: z.B. Unit 2',
            'maxlength': '50'
        }
    ))
    descirption = forms.CharField(required=False, label='', empty_value='', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'style': 'width: 100%;float:left; margin-top:1rem;',
            'placeholder': 'Beschreibung: z.B. Für Test von Unit 2',
            'maxlength': '255'
        }
    ))

    class Meta:
        model = LernSet
        fields =['name', 'descirption']

class CardForm(forms.ModelForm):
    txt_front = forms.CharField(label='', empty_value='Hallo', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'style': 'width: 100%; vertical-align: middle; margin: 5px 10px 5px 0; padding: 10px; background-color: #fff; border: 1px solid #ddd;display: inline;',
            'placeholder': 'Übersetzung/Wort z.B. Stuhl',
            'maxlength': '100'
        }
    ))
    txt_back = forms.CharField(label='', empty_value='Hallo', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'style': 'width: 100%; vertical-align: middle; margin: 5px 10px 5px 0; padding: 10px; background-color: #fff; border: 1px solid #ddd;display: inline;',
            'placeholder': 'Übersetzung/Wort z.B. chair',
            'maxlength': '100'
        }
    ))
    donkey_bridge = forms.CharField(required=False, label='', empty_value='', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'style': 'width: 100%; vertical-align: middle; margin: 5px 10px 5px 0; padding: 10px; background-color: #fff; border: 1px solid #ddd;display: inline;',
            'placeholder': 'eine Eselsbrücke / Abstand:keine Eselsbrücke',
            'maxlength': '80'
        }
    ))
    class Meta:
        model = LernKarte
        fields =['txt_front', 'txt_back', 'donkey_bridge']