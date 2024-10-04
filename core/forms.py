from django import forms

class EnterPublicLink(forms.Form):
    public_link = forms.CharField(label='Input public link fron yandex disk', max_length=255)

    