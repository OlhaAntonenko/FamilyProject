from django import forms

from FamilyStorage import settings
from Person.models import PersonModel


class PersonModelForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,
                                    help_text='DD/MM/YYYY', required=False)
    date_of_death = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,
                                    help_text='DD/MM/YYYY', required=False)

    def __init__(self, *args, **kwargs):
        super(PersonModelForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            user = kwargs['initial']['user']
            event = kwargs['initial'].get('event')

            mother_queryset = PersonModel.objects.filter(user=user)
            if event:
                mother_queryset = mother_queryset.exclude(id=kwargs['initial']['event'].id)

            self.fields['mother'].queryset = mother_queryset

            father_queryset = PersonModel.objects.filter(user=user)
            if event:
                father_queryset = father_queryset.exclude(id=kwargs['initial']['event'].id)

            self.fields['father'].queryset = father_queryset

    class Meta:
        model = PersonModel
        fields = '__all__'
