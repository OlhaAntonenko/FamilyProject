from django.urls import path

from Person.views import download, PersonCreate, PersonDelete, PersonInfoView, PersonListView

urlpatterns = [
    path('', PersonListView.as_view(), name='all_persons'),
    path('add/', PersonCreate.as_view(), name='add_person'),
    path('<int:pk>/', PersonInfoView.as_view(), name='person_info'),
    path('<int:pk>/delete/', PersonDelete.as_view(), name='delete_person'),
    path('<int:pk>/download/', download, name='download_person_info'),
]
