from django.urls import path, include
from rest_framework import routers
from .views import (
    LoginTemplateView, LoginView, LogoutView, MeView, browser_logout,
    ProviderViewSet, ConsumerViewSet
)

router = routers.DefaultRouter()
router.register(r'providers', ProviderViewSet, basename='provider')
router.register(r'consumers', ConsumerViewSet, basename='consumer')

urlpatterns = [
    # Auth routes
    path("auth/me/", MeView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    path("auth/login-page/", LoginTemplateView.as_view(), name="login-page"),
    path("logout/", browser_logout, name="browser-logout"),
    path("api/auth/logout/", LogoutView.as_view()),

    # Provider and Consumer API routes
    path("", include(router.urls)),  # router at root
]
