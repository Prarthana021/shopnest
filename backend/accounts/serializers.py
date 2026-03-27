from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Handles turning raw JSON (email, password, name) into a User object.

    WHY use a serializer instead of writing the view logic directly?
    Serializers do two things: validate input data and convert between Python
    objects and JSON. Keeping this logic here (not in the view) means the view
    stays thin — it just calls serializer.save() and returns a response.

    WHY write_only=True on password?
    We never want to send the password back in a response, even hashed.
    write_only ensures it can come IN but never goes OUT.
    """

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        # create_user() hashes the password before saving.
        # If we used User.objects.create() directly, the password would be stored
        # as plain text — a critical security bug.
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Read-only representation of a user (returned after login/register)."""

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')
