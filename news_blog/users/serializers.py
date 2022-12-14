from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for registration"""
    # Make first_name and last_name fields required
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    password_confirm = serializers.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'password', 'password_confirm']

    def validate(self, data):
        """Check that password and password_confirm are same"""
        # remove non-model field from data
        password_confirm = data.pop('password_confirm', None)

        if data['password'] != password_confirm:
            raise serializers.ValidationError('Password confirmation is wrong')

        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user
