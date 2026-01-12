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

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, ProvidedOffer
from .serializers import ProviderSerializer, ConsumerSerializer

class ProviderViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProviderSerializer

    @action(detail=True, methods=['post'], url_path='set-provided-offers')
    def set_provided_offers(self, request, pk=None):
        user = self.get_object()
        offer_ids = request.data.get('offer_ids', [])
        if not isinstance(offer_ids, list):
            return Response({"error": "offer_ids must be a list"}, status=400)

        created_offers = []
        for offer_id in offer_ids:
            obj, created = ProvidedOffer.objects.get_or_create(
                user=user,
                offer_id=offer_id
            )
            if created:
                created_offers.append(str(offer_id))

        return Response({
            "status": "provided_offer_ids added",
            "added_offer_ids": created_offers
        })

    @action(detail=True, methods=['get'], url_path='get-provided-offers')
    def get_provided_offers(self, request, pk=None):
        user = self.get_object()
        offer_ids = list(user.provided_offers.values_list('offer_id', flat=True))
        return Response({"provided_offer_ids": offer_ids})


class ConsumerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ConsumerSerializer

    @action(detail=True, methods=['post'])
    def set_consumed_offers(self, request, pk=None):
        user = self.get_object()
        offer_ids = request.data.get('offer_ids', [])
        if not isinstance(offer_ids, list):
            return Response({"error": "offer_ids must be a list"}, status=400)
        user.consumed_offer_ids = offer_ids
        user.is_consumer = True
        user.save()
        return Response({"status": "consumed_offer_ids set", "consumed_offer_ids": offer_ids})

    @action(detail=True, methods=['get'])
    def get_consumed_offers(self, request, pk=None):
        user = self.get_object()
        return Response({"consumed_offer_ids": user.consumed_offer_ids})
