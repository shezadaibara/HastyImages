"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from invitation import views as invitation_views
from gallery import views as gallery_views
from rest_framework import routers
from gallery.views import FilePolicyAPI, FileUploadCompleteHandler
from django.views.generic.base import TemplateView


router = routers.DefaultRouter()
router.register(r'invitation', invitation_views.InvitationViewSet)
router.register(r'images', gallery_views.ImagesViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/upload/', TemplateView.as_view(template_name='upload.html'), name='upload-home'),
    path('api/files/policy/', FilePolicyAPI.as_view(), name='upload-policy'),
    path('api/files/complete/', FileUploadCompleteHandler.as_view(), name='upload-complete'),
]
