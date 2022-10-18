from rest_framework import serializers
from reviews.models import User
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=(
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                    'role',
                    'bio'
                )
            )
        ]


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=(
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'bio'
        )
        read_only_fields = ('role',)

class RegistraterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            )
        ]
    )
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            )
        ]
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Username "me" is not valid')
        return value

    class Meta:
        model = User
        fields = ('username', 'email')

class TokenUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
