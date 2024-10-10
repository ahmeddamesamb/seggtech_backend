from rest_framework import serializers

from .models import User, Mesure


class UserSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'nom', 'telephone', 'photo']

    def get_photo_url(self, obj):
        request = self.context.get('request')
        if obj.photo:
            return request.build_absolute_uri(obj.photo.url)
        return None


class MesureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesure
        fields = ['temperature', 'tds', 'turbidite', 'ph', 'conductivite', 'oxygene', 'timestamp']
