from django import forms
from .models import *

class add_daneshjoo_form(forms.Form):
    name = forms.CharField()
    gender_choice = (
        ("male" , "male"),
        ("female" , "female"),
    )
    gender = forms.ChoiceField(choices=gender_choice)
    def clean(self):
        cd = self.cleaned_data
        daneshjoos = Daneshjoo.objects.all()
        for d in daneshjoos:
            if d.name == cd.get('name'):
                self.add_error('name', f"{d.name} تکراری است.")     
        return cd

class add_daneshjoo_form2(forms.Form):
    names = forms.CharField(widget=forms.Textarea)
    def clean(self):
        cd = self.cleaned_data
        daneshjoos = Daneshjoo.objects.all()
        for d in daneshjoos:
            if d.name == cd.get('name'):
                self.add_error('name', f"{d.name} تکراری است.")     
        return cd

class add_friend_form(forms.Form):
    choices = []
    choices.append(('', '---دوست مورد نظر را انتخاب کنید---'))
    for d in Daneshjoo.objects.all():
        choices.append((f'{d.name}',f'{d.name}'))
    choices = tuple(choices)
    friend = forms.ChoiceField(choices=choices)
    def clean(self):
        cd = self.cleaned_data
        daneshjoos = Daneshjoo.objects.all()
        c=0
        for d in daneshjoos:
            if d.name == cd.get('friend'):
                c+=1
        if not c:
            f = cd.get('friend')
            self.add_error('friend', f"{f} وجود ندارد.")     
        return cd