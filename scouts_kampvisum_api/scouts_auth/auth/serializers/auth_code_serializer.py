from rest_framework import serializers


class AuthCodeSerializer(serializers.Serializer):
    authCode = serializers.CharField()
    redirectUri = serializers.CharField()
