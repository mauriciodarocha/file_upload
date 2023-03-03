"""file_upload URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
# from django.views.generic import TemplateView

# from apps.pages.views import home_page
from apps.frontend.views import FrontendView
from apps.file_upload.views import (file_upload_view, upload_file, files_list,
                                    upload_file_post, get_auth_token)

urlpatterns = [
    path('media_files/', files_list, name='file list'),
    path('upload/', upload_file, name='upload file'),
    path('upload_file_post/', upload_file_post, name='upload file'),
    path('upload_form/', file_upload_view, name='file upload'),
    path('get_token/', get_auth_token),
    path('admin/', admin.site.urls),
    # path('', home_page, name='Home'),
    path('', FrontendView.as_view(), name='Home'),
    # re_path(
    #     r"^.*$",
    #     # TemplateView.as_view(template_name="base.html")
    #     FrontendView.as_view()
    # ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
