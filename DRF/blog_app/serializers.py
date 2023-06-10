import re

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AuthUsers, Blog
from .register import generate_username


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=255, min_length=6, write_only=True)

    class Meta:
        model = AuthUsers
        fields = ["email", "first_name", "last_name", "password"]

    def save(self):
        first_name = self.validated_data.get("first_name", " ")
        last_name = self.validated_data.get("last_name", " ")
        name = first_name + " " + last_name

        user = AuthUsers(
            email=self.validated_data["email"],
            first_name=first_name,
            last_name=last_name,
            password=self.validated_data["password"],
            username=generate_username(name),
        )
        user.set_password(self.validated_data["password"])
        user.save()
        return user


class LoginSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=5)
    password = serializers.CharField(max_length=255, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=5, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = AuthUsers.objects.get(email=obj["email"])
        return {"refresh": user.tokens()["refresh"], "access": user.tokens()["access"]}

    class Meta:
        model = AuthUsers
        fields = ["id", "email", "password", "tokens", "username"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = authenticate(username=email, password=password)

        if not user:
            raise AuthenticationFailed(_("Invalid Credentials"))

        # check password with regex
        if not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            password,
        ):
            raise serializers.ValidationError(
                _(
                    "Password must contain at least 8 characters, 1 uppercase, 1 lowercase, 1 number and 1 special character"
                )
            )

        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "token": user.tokens(),
        }
        # return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {_("invalid_token"): _("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs.get("refresh")
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except Exception:
            self.fail(_("Invalid token"))


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["id", "title", "content", "display_picture"]
