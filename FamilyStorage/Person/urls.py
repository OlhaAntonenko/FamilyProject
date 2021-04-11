from django.urls import path

from Person.views import PersonCreate, PersonDelete, PersonInfoView, PersonListView, PersonUpdate

urlpatterns = [
    path('', PersonListView.as_view(), name='all_persons'),
    path('add/', PersonCreate.as_view(), name='add_person'),
    path('<int:pk>/', PersonInfoView.as_view(), name='person_info'),
    path('<int:pk>/update/', PersonUpdate.as_view(), name='update_person'),
    path('<int:pk>/delete/', PersonDelete.as_view(), name='delete_person'),
]
