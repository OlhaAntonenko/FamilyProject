from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


class PersonModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=150, default='')
    last_name = models.CharField(max_length=150, default='', blank=True)
    patronymic_name = models.CharField(max_length=150, default='', blank=True)
    gender = models.CharField(max_length=6, blank=True,
                              choices=[('Male', 'Male'), ('Female', 'Female')])
    date_of_birth = models.DateField(null=True, blank=True, help_text='DD/MM/YYYY')
    date_of_death = models.DateField(null=True, blank=True, help_text='DD/MM/YYYY')
    info = models.TextField(max_length=1000, default='', blank=True)
    place_of_birth = models.CharField(max_length=150, default='', blank=True)
    place_of_death = models.CharField(max_length=150, default='', blank=True)
    mother = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,
                               related_name='mother_children')
    father = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,
                               related_name='father_children')
    # photos = models.ImageField(upload_to='photos/', null=True, blank=True, height_field=100, width_field=100)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        res = self.first_name
        res += f' {self.patronymic_name}' if self.patronymic_name else ''
        res += f' {self.last_name}' if self.last_name else ''
        return res

    def get_absolute_url(self):
        return reverse('person_info', args=[self.id])

    @property
    def siblings(self):
        siblings = set()

        if self.mother:
            siblings.update([person for person in self.mother.mother_children.all()])
        if self.father:
            siblings.update([person for person in self.father.father_children.all()])

        return [person for person in siblings if person != self]

    @property
    def children(self):
        children = set()
        children.update([person for person in self.mother_children.all()])
        children.update([person for person in self.father_children.all()])
        return children

    def get_data(self) -> dict:
        data = {f.verbose_name: getattr(self, f.attname) for f in self._meta.concrete_fields}

        not_to_show = ['ID', 'user']
        for field in not_to_show:
            if field in data:
                del data[field]

        to_str = ['date of birth', 'date of death']
        for field in to_str:
            if field in data:
                data[field] = str(data.get(field) or '')

        person_id_to_str_name = ['mother', 'father']
        for field in person_id_to_str_name:
            needed_id = data.get(field)
            if needed_id:
                data[field] = str(PersonModel.objects.get(id=needed_id))

        return data
