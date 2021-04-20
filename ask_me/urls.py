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
from django.contrib import admin
from django.urls import path

from app import views

# cписок новых вопросов (главная страница) (URL = /)
# cписок “лучших” вопросов (URL = /hot/)
# cписок вопросов по тэгу (URL = /tag/blablabla/)
# cтраница одного вопроса со списком ответов (URL = /question/35/)
# форма логина (URL = /login/)
# форма регистрации (URL = /signup/)
# форма создания вопроса (URL = /ask/)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('<int:page_no>', views.index),
    path('hot/', views.hot),
    path('hot/<int:page_no>/', views.hot, name="hot"),
    path('tag/<int:tag_id>/', views.tag),
    path('tag/<int:tag_id>/<int:page_no>/', views.tag, name="tag"),
    path('question/<int:question_id>/', views.question),
    path('question/<int:question_id>/<int:page_no>/', views.question, name="question"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('ask/', views.ask, name="ask"),
    path('setting/', views.setting, name="setting")
]
