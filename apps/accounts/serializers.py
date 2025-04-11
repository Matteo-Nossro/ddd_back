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