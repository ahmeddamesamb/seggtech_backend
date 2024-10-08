import json

from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *
from .serializers import *


@api_view(['GET', 'POST'])
def mesure_list(request):
    if request.method == 'GET':
        mesures = Mesure.objects.all()
        serializer = MesureSerializer(mesures, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MesureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def mesure_detail(request, id):
    try:
        mesure = Mesure.objects.get(pk=id)
    except Mesure.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MesureSerializer(mesure)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MesureSerializer(mesure, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        mesure.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])  # Hacher le mot de passe ici
            user.save()  # Enregistrer l'utilisateur avec le mot de passe haché
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            user = serializer.save(commit=False)  # Utiliser commit=False pour éviter d'enregistrer avant le hachage
            if 'password' in request.data and request.data['password']:  # Vérifier si un mot de passe a été fourni
                user.set_password(request.data['password'])  # Hacher le nouveau mot de passe
            user.save()  # Enregistrer l'utilisateur
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def archive_user(request, id):
    try:
        user = User.objects.get(id=id)
        user.is_active = False
        user.save()
        return Response({'status': 'User archived successfully'})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    except Exception as e:
        print(f"Erreur lors de l'archivage de l'utilisateur : {e}")
        return Response({'error': 'An error occurred'}, status=500)


@api_view(['PUT'])
def activate_user(request, id):
    try:
        user = User.objects.get(id=id)
        user.is_active = True
        user.save()
        return Response({'status': 'User activated successfully'})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if email is None or password is None:
        return Response({'error': 'Please provide both email and password.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, email=email, password=password)
    if user is not None:
        if user.is_active:
            refresh = RefreshToken.for_user(user)
            # Vérifie si l'URL de la photo est valide
            photo_url = user.photo.url if user.photo else None  # Utilise le bon champ ici

            user_data = {
                'email': user.email,
                'nom': user.nom,
                'telephone': user.telephone,
                'photo': photo_url,  # Renvoie l'URL ou None
                'is_active': user.is_active,
            }
            return Response({
                'refresh': str(refresh),
                'token': str(refresh.access_token),
                'user': user_data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'This account is inactive.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'error': 'Incorrect email or password'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_view(request):
    try:
        token = request.data.get('token')
        if not token:
            return Response({'error': 'No access token provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token_obj = AccessToken(token)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        if hasattr(token_obj, 'blacklist'):
            token_obj.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Token is not valid for blacklisting'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def store_sensor_data(request):
    if request.method == 'POST':
        try:
            print("Requête reçue:", request.body)
            data = json.loads(request.body)
            id_counter = cache.get('sensor_data_id_counter', 1)
            cache.set('sensor_data_id_counter', id_counter + 1)
            data['id'] = id_counter
            cache_key = f"sensor_data:{id_counter}"
            cache.set(cache_key, data, timeout=60)
            return Response({"message": "Données des capteurs stockées avec succès", "id": id_counter},
                            status=status.HTTP_201_CREATED)

        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Méthode non autorisée"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_sensor_data(request):
    sensor_data = []

    for key in cache.keys('sensor_data:*'):
        data = cache.get(key)
        if data:
            sensor_data.append(data)

    if sensor_data:
        return Response(sensor_data, status=status.HTTP_200_OK)
    return Response({'error': 'Data not found'}, status=status.HTTP_404_NOT_FOUND)
