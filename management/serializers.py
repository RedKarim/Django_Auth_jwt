from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    security_code = serializers.CharField(required=False)

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()