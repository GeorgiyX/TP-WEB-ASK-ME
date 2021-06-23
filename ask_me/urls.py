"""ask_me URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import ask_me.settings
from app import views
import app.constants as constants
import ask_me.settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name=constants.INDEX_URL),
    path('<int:page_no>', views.index, name=constants.INDEX_URL),
    path('hot/', views.hot, name=constants.HOT_URL),
    path('hot/<int:page_no>/', views.hot, name=constants.HOT_URL),
    path('tag/<int:tag_id>/', views.tag, name=constants.TAG_URL),
    path('tag/<int:tag_id>/<int:page_no>/', views.tag, name=constants.TAG_URL),
    path('question/<int:question_id>/', views.question, name=constants.QUESTION_URL),
    path('question/<int:question_id>/<int:page_no>/', views.question, name=constants.QUESTION_URL),
    path('login/', views.login, name=constants.LOGIN_URL),
    path('signup/', views.signup, name=constants.SIGNUP_URL),
    path('logout/', views.logout, name=constants.LOGOUT_URL),
    path('ask/', views.ask, name=constants.ASK_URL),
    path('setting/', views.setting, name=constants.SETTING_URL)
]
if ask_me.settings.DEBUG:
    urlpatterns += static(ask_me.settings.MEDIA_URL, document_root=ask_me.settings.MEDIA_ROOT)
