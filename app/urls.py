from django.urls import path
import app.views
import app.forms
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls import url
from datetime import datetime

urlpatterns = [
    path("", app.views.home, name="home"),
    path("textShow/<int:id>/", app.views.textShow, name='textShow'),
    path("testShow/<int:id>/", app.views.testShow, name='testShow'),
    path("generation/", app.views.generation, name='generation'),
    path("textLoad/", app.views.textLoad, name='textLoad'),
    path('getText/<int:id>/', app.views.getText),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("register/", app.views.register, name='register'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=app.forms.BootstrapAuthenticationForm,
             extra_context={
                 'title': 'Log in',
                 'year': datetime.now().year,
             }
         ),
         name='login'),
]
