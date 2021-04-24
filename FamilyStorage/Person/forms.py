from django import forms

from Person.models import PersonModel


class PersonModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PersonModelForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            user = kwargs['initial']['user']
            self.fields['mother'].queryset = PersonModel.objects.filter(user=user)
            self.fields['father'].queryset = PersonModel.objects.filter(user=user)

    class Meta:
        model = PersonModel
        fields = '__all__'
