"""
URL configuration for finapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include

from registration import views as registration_views
from main import views as main_views

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('', main_views.index, name='home'),
    path('registration/', registration_views.register_view, name='register'),
    path('make-profile/', registration_views.make_profile, name='make_profile'),
    path('login/', registration_views.login_view, name='login'),
    path('income/', main_views.income_page, name='income'),
    path('expenses/', main_views.expenses_page, name='expenses'),
    path('budget/', main_views.budget_page, name='budget'),
    path('profile/', main_views.profile_page, name='profile'),
    path('logout/', registration_views.logout_view, name='logout'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('get-subcategories/', main_views.get_subcategories, name='get_subcategories'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
