from django.urls import path

from user.views import login, signup


app_name = "user"
urlpatterns = [
    path("login/", login,name="login"),
    path("signup/", signup,name="signup"),

]
