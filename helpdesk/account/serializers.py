from django.contrib.auth.models import User
# from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='Такой email уже зарегистрирован')],
        label='Электронная почта',
    )
    password = serializers.CharField(
        max_length=100,
        write_only=True,
        required=True,
        label='Пароль',
        # validators=[validate_password]
    )
    password2 = serializers.CharField(
        max_length=100,
        write_only=True,
        required=True,
        label='Подтвердите пароль',)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'Password': 'Пароли не совпадают'}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('user', 'tel', 'office', 'position', 'department', 'type')

    def create(self, validated_data):
        user = UserSerializer(data=validated_data.pop('user'))
        user.is_valid(raise_exception=True)
        user = user.save()
        validated_data.update({'user_id': user.id})
        return super().create(validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(
        max_length=100,
        write_only=True,
        required=True,
        label='Старый пароль'
    )
    new_password = serializers.CharField(
        max_length=100,
        write_only=True,
        required=True,
        label='Новый пароль'
    )
