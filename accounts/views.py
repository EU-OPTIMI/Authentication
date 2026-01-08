from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from rest_framework import permissions, status, views
from rest_framework.response import Response
from django.shortcuts import redirect


class MeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            }
        )


class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username") or request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)  # sets session cookie
        return Response({"detail": "ok"})


class LogoutView(views.APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "ok"})


class LoginTemplateView(TemplateView):
    template_name = "accounts/login.html"



def browser_logout(request):
    logout(request)
    next_url = request.GET.get("next", "/")
    return redirect(next_url)    
