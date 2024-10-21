from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator, ValidationError
from django.contrib.auth.password_validation import validate_password
import re

class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})

        if len(attrs['password']) < 13:
            raise serializers.ValidationError({"password_too_short": "Le mot de passe doit au minimum contenir 13 caractères."})

        if not re.findall(r'[A-Z]', attrs['password']):
            raise serializers.ValidationError( {"password_no_upper":"Le mot de passe doit contenir au moins une lettre majuscule."})

        if not re.findall(r'[a-z]', attrs['password']):
            raise serializers.ValidationError({"password_no_lower":"Le mot de passe doit contenir au moins une lettre minuscule."})

        if not re.findall(r'[0-9]', attrs['password']):
            raise serializers.ValidationError({"password_no_digit":"Le mot de passe doit contenir au moins un chiffre."})

        if not re.findall(r'[!@#$%^&*(),.?":{}|<>]', attrs['password']):
            raise serializers.ValidationError({"password_no_special":"Le mot de passe doit contenir au moins un caractère spécial."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class AuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auteur
        fields = '__all__'
        

class LivreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livre
        fields = '__all__'

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

class ExemplaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exemplaire
        fields = '__all__'

class EmpruntSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprunt
        fields = '__all__'

class CommentaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        fields = '__all__'

class EditeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editeur
        fields = '__all__'

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'
