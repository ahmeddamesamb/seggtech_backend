from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()  # Champ personnalisé pour l'URL complète

    class Meta:
        model = User
        fields = ['email', 'nom', 'telephone', 'photo']  # Inclure 'photo_url' dans les champs

    def get_photo_url(self, obj):
        request = self.context.get('request')  # Récupère l'objet request depuis le contexte
        if obj.photo:  # Vérifie si une photo est présente
            return request.build_absolute_uri(obj.photo.url)  # Génère l'URL complète avec le domaine
        return None
