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
    # siblings = models.ManyToManyField("self", blank=True)
    # photos = models.ImageField(upload_to='photos/', null=True, blank=True, height_field=100, width_field=100)

    # files = models.FileField()

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f'{self.last_name or ""} {self.first_name or ""} {self.patronymic_name or ""}'

    def get_absolute_url(self):
        return reverse('person_info', args=[self.id])
