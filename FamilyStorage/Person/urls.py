from django.urls import path

from Person.views import all_persons, person_info


urlpatterns = [
    path('', all_persons, name='all_persons'),
    path('<int:pid>/', person_info, name='person_info'),
]
