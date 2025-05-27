"""
URL configuration for AI_Notebook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from . import views
from .views import summarize_flashcard_qa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('chat/', views.chat, name='chat'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/process/', views.dashboard_process, name='dashboard_process'),  # Add this line
    path('summarize/', summarize_flashcard_qa, name='summarize'),
    path('flashcards/', views.summarize_flashcard_qa, name='flashcards'),
    path('logout/', views.login_view, name='logout'),
    path('upload/', views.upload_file, name='upload_file'),
]