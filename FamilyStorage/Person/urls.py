from django.urls import path
from django.conf.urls import url

from Person.views import delete_person, PersonListView, person_info, update_person_info


urlpatterns = [
    path('', PersonListView.as_view(), name='all_persons'),
    path('<int:pid>/', person_info, name='person_info'),
    path('<int:pid>/update_<str:field>', update_person_info, name='update_person_info'),
    path('<int:pid>/delete_person', delete_person, name='delete_person'),
]
