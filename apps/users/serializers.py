from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'password', 'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth'
        ]

    def save(self):
        user = User(email=self.data['email'],
                    username=self.data['username'],
                    phone_number=self.data['phone_number'],
                    first_name=self.data['first_name'],
                    last_name=self.data['last_name'],
                    date_of_birth=self.data['date_of_birth'])
        password = self.data['password']
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'password', 'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth'
        ]


class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(
        write_only=True
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
