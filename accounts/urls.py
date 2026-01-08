from django.urls import path

from .views import LoginTemplateView, LoginView, LogoutView, MeView, browser_logout
urlpatterns = [
    path("auth/me/", MeView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    path("auth/login-page/", LoginTemplateView.as_view(), name="login-page"),
    path("logout/", browser_logout, name="browser-logout"),
    path("api/auth/logout/", LogoutView.as_view()),
]
