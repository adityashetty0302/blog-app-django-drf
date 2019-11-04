from rest_framework import serializers
from django.contrib.auth import (get_user_model, )
from rest_framework.exceptions import ValidationError
from django.db.models import Q

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label="Email address")
    email2 = serializers.EmailField(label="Confirm email")

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'email2']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

    def validate_email(self, value):
        email = value
        user_qs = User.objects.filter(email=email)
        if user_qs:
            raise serializers.ValidationError("Already Registered")

        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        email2 = value

        if email1 != email2:
            raise serializers.ValidationError("Emails must match")

        return value


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(label="Email address", required=False,
                                   allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'token', ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        username = data.get("username", None)
        password = data["password"]

        if not email and not username:
            raise ValidationError("A username or email is reqd to login")

        user = User.objects.filter(
            Q(email=email) | Q(username=username)).distinct()

        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials.")

        data["token"] = "SOME RANDOM TOKEN"
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
