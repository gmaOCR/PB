"""
URL configuration for PorteFolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf.urls.static import static

from IFCextract import views as ifc_views
from Photos import views as ph_views
from Profiles import views as pr_views

urlpatterns = [
    path('login/', pr_views.CustomLoginView.as_view(), name='login'),
    path('home/', ph_views.home, name='home'),
    path('', ph_views.home, name='home'),

    path('photo/add', ph_views.add_photo, name='add_photo'),
    path('photo/edit/<int:photo_id>', ph_views.edit_photo, name='edit_photo'),
    path('photo/del/<int:photo_id>', ph_views.delete_photo, name='delete_photo'),

    path('ifc/upload/read/', ifc_views.read_ifc, name='upload_ifc'),
    path('ifc/upload/extract/', ifc_views.extract_geometry, name='extract_ifc'),
    path('ifc/upload/viewer/', ifc_views.preview_ifc, name='preview_ifc'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
