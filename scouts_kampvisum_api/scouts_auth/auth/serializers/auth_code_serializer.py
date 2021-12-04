from rest_framework import serializers

# The member fields dont follow standard snake case python standard to
# keep oidc bundles consistent between django and symfony
class AuthCodeSerializer(serializers.Serializer):
    authCode = serializers.CharField()
    redirectUri = serializers.CharField()
