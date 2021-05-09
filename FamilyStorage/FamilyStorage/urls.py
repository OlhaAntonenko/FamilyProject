"""FamilyStorage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from FamilyStorage.views import (
    UserDelete, UserInfoView, UserUpdate, connections_page, main_page, sign_up
)

urlpatterns = [
    path('', main_page, name='main_page'),
    path('admin/', admin.site.urls),
    path('connections/', connections_page, name='connections'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sign_up/', sign_up, name='sign_up'),
    path('account/', UserInfoView.as_view(), name='account'),
    path('account/update/', UserUpdate.as_view(), name='update_user'),
    path('account/delete/', UserDelete.as_view(), name='delete_user'),
]

urlpatterns += [
    path('people/', include('Person.urls'))
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

