from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from core.validators import min_length

USER_MODEL = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(write_only=True, validators=[min_length])

    class Meta:
        model = USER_MODEL
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, data):
        validate_password(data)
        return data

    def validate_password_repeat(self, data):
        if data != self.initial_data.get('password'):
            raise serializers.ValidationError('Пароли не одинаковые')
        return data

    def create(self, validated_data):
        validated_data.pop('password_repeat')
        user = USER_MODEL.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ('username', 'password')


class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        read_only_fields = ('id',)


class UserChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, validators=[min_length])
    new_password = serializers.CharField(write_only=True, validators=[min_length])

    class Meta:
        model = USER_MODEL
        fields = ('old_password', 'new_password')

    def validate_password(self, data):
        validate_password(data)
        return data

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data.get('old_password')):
            raise serializers.ValidationError({'old_password': ['Неверный пароль']})

        instance.set_password(validated_data.get('new_password'))
        instance.save()

        return instance
