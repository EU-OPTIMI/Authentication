from rest_framework import serializers
from .models import User

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'provider_id', 'provided_offer_ids']

class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'consumer_id', 'consumed_offer_ids']
