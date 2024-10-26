from rest_framework import serializers

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class SecurityCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    security_code = serializers.CharField()

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()

