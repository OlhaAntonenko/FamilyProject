from django.db import models
from django.shortcuts import reverse


class PersonModel(models.Model):
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True)
    patronymic_name = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=1, default='N',
                              choices=[('M', 'Male'), ('F', 'Female'), ('N', 'NotKnown')])
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    info = models.TextField(max_length=1000, null=True, blank=True)
    place_of_birth = models.CharField(max_length=150, null=True, blank=True)
    place_of_death = models.CharField(max_length=150, null=True, blank=True)
    # photos = models.ImageField()  TODO: main photo?
    # files = models.FileField()

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f'{self.last_name or ""} {self.first_name or ""} {self.patronymic_name or ""}'

    def get_absolute_url(self):
        return reverse('person_info', args=[self.id])
