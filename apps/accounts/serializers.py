from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=[('citizen', 'Citizen'), ('scientist', 'Scientist'), ('admin', 'Admin')],
        required=True,
        write_only=True  # On indique que ce champ est uniquement en écriture.
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role')
        validated_data.pop('password2')

        # Créer l'utilisateur
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        # Ajouter l'utilisateur au groupe correspondant
        try:
            group = Group.objects.get(name=role)
        except Group.DoesNotExist:
            group = None
        if group:
            user.groups.add(group)

        return user

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Ajouter des claims personnalisés
        token['username'] = user.username

        # Récupérer le rôle (groupe) de l'utilisateur
        groups = user.groups.all()
        if groups.exists():
            token['role'] = groups.first().name
        else:
            token['role'] = 'no_role'

        return token

# apps/accounts/serializers.py (ajoutez ceci à votre fichier existant)

class UserManagementSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined', 'last_login', 'is_active', 'role')

    def get_role(self, obj):
        # Récupérer le premier groupe de l'utilisateur comme son rôle
        groups = obj.groups.all()
        if groups.exists():
            return groups.first().name
        return 'no_role'

class UserUpdateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=[('citizen', 'Citizen'), ('scientist', 'Scientist'), ('admin', 'Admin')],
        required=True
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_active', 'role')

    def update(self, instance, validated_data):
        role = validated_data.pop('role', None)

        # Mettre à jour les champs de base
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        # Mettre à jour le rôle si spécifié
        if role:
            # Supprimer tous les groupes actuels
            instance.groups.clear()
            # Ajouter au nouveau groupe
            try:
                group = Group.objects.get(name=role)
                instance.groups.add(group)
            except Group.DoesNotExist:
                pass

        return instance