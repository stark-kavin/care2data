from django.urls import path
from .views import *

urlpatterns = [
    path("login/",login_view,name="login"),
    path("",home_view,name="home"),
    path("edit/<id>/",edit_view,name="edit"),
    path("create/",create_view,name="create"),
    path("reset/",reset_view,name="reset"),
    path("sponser/",sponser_view,name="sponser"),
    path("logout/",logout_view,name="logout")
]
