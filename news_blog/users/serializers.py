from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.settings import api_settings

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for registration"""

    password_confirm = serializers.CharField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username",
                  "password", "password_confirm"]

    def validate(self, data):
        """
        Проверить похоже ли подтверждение пароля на сам пароль.
        Провести валидацию пароля с помощью валидатора django.
        """
        # убрать из data password_confirm не являющийся полем User
        password_confirm = data.pop("password_confirm", None)

        if data["password"] != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": "Подтверждение пароля неверное."}
            )

        # валидация пароля
        user = User(**data)
        password = data.get("password")

        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]} # noqa
            )

        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user
