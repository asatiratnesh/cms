from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, ContentItem
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
import base64
from django.core.files.base import ContentFile

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('phone', 'address', 'city', 'state', 'country', 'pincode')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'is_staff','profile')

    def create(self, validated_data):

        # create user 
        user = User.objects.create(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            password = make_password(validated_data['password']),
            is_staff = validated_data['is_staff'],
        )

        profile_data = validated_data.pop('profile')
        profile = Profile.objects.create(
            user = user,
            phone = profile_data['phone'],
            address = profile_data['address'],
            state = profile_data['state'],
            city = profile_data['city'],
            country = profile_data['country'],
            pincode = profile_data['pincode'],
        )

        return user


class Base64ImageField(serializers.ImageField):
    def from_native(self, data):
        if isinstance(data, basestring) and data.startswith('data:image'):
            # base64 encoded image - decode
            format, imgstr = data.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]  # guess file extension

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super(Base64ImageField, self).from_native(data)


class ContentItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ContentItem
        fields = ('title', 'body', 'summary', 'doc', 'categories')


class ContentItemSearchSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ContentItem
        fields = ('title', 'body', 'summary', 'categories')