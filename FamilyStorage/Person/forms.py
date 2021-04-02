from django import forms

from Person.models import PersonModel


class PersonModelForm(forms.ModelForm):
    class Meta:
        model = PersonModel
        fields = '__all__'
