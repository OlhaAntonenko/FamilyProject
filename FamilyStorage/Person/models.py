from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError


def photo_file_name(instance, *args, **kwargs):
    photo_type = ''

    if args:
        uploaded_file = args[0]
        uploaded_type = uploaded_file.partition('.')[2]
        if uploaded_type:
            photo_type = uploaded_type

    return f'photos/{slugify(str(instance))}.{photo_type}'


def validate_image(image):
    file_size = image.file.size
    limit_mb = 5
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Max size of file is {limit_mb} MB")


class PersonModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=150, default='')
    last_name = models.CharField(max_length=150, default='', blank=True)
    patronymic = models.CharField(max_length=150, default='', blank=True)
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
    photo = models.ImageField(upload_to=photo_file_name, null=True, blank=True,
                              validators=[validate_image])  # TODO: remove not used images

    class Meta:
        ordering = ["last_name", "first_name"]

    ADDITIONAL_FIELDS = ['siblings', 'children']

    def __str__(self):
        res = self.first_name
        res += f' {self.patronymic}' if self.patronymic else ''
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
        return list(children)

    def get_data(self) -> dict:
        data = {f.verbose_name: getattr(self, f.attname) for f in self._meta.concrete_fields}
        for field in self.ADDITIONAL_FIELDS:
            data[field] = getattr(self, field, None)

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

        if data.get('photo'):  # TODO: change hardcode
            data['photo'] = data['photo'].path

        return data
