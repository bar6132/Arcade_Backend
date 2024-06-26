from django.shortcuts import render
from rest_framework import status
from django.db import IntegrityError
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Game, UserProfile, ContactMsg, Message
from .serializers import GameSerializer, UserProfileSerializer, ContactMsgSerializer, MessageSerializer, UserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.core.cache import cache
from django.http import JsonResponse
from .my_buto import generate_presigned_url, upload_file_to_s3, get_image_url_from_s3


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def my_view(request):
    user = request.user
    response_data = {
        'username': user.username,
    }
    return Response(response_data)


@api_view(['GET', 'PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])
def manage_users(request):
    """The function allows you to access and manage all users.
    You have the option to delete a user or promote them to a super user."""
    if request.method == 'GET':
        users = User.objects.all()
        user_data = []
        for user in users:
            user_data.append({
                'id': user.id,
                'username': user.username,
                'is_superuser': user.is_superuser,
            })
        return Response(user_data)

    if request.method == 'PATCH':
        user_id = request.data.get('user_id')
        is_superuser = request.data.get('is_superuser')

        try:
            user = User.objects.get(id=user_id)
            user.is_superuser = is_superuser
            user.save()
            return Response({'message': 'Superuser status updated successfully.'})
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=404)

    if request.method == 'DELETE':
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({'message': 'User deleted successfully.'})
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=404)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_user_data(request):
    """The function takes user data as input
    and returns the user information."""
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    user_data = {
        'username': user.username,
        'is_superuser': user.is_superuser,
    }
    response_data = {
        'user': user_data,
        'id': user_profile.id,
        'email': user_profile.email,
        'location': user_profile.location,
        'age': user_profile.age,
        'phone': user_profile.phone,
        'phonecontact': user_profile.phonecontact,
        'emailcontact': user_profile.emailcontact,
        'webcontact': user_profile.webcontact,
        
    }
    return Response(response_data)


@api_view(['GET', 'PUT'])
def get_profile(request, pk):
    """The function retrieves the user profile based on the provided ID. 
    It displays the profile information and allows you to make edits to the profile."""
    try:
        profile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

@api_view(['GET'])
def uploader_data(request, pk):
    """The function retrieves the information
    of the game uploader based on their ID."""            

    try:
        profile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        return Response(status=404)
    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
def get_user(request, pk):
    """The function return the user by their ID."""

    profile = User.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = UserSerializer(profile)
        print(serializer.data)
        return Response(serializer.data)


@api_view(['GET'])
def games(request, pk=None):
    """
    The function
    Get all games or one only
    """
    if request.method == 'GET':
        if pk is None:
            g = Game.objects.all()
            serializer = GameSerializer(g, many=True)
            serialized_data = serializer.data

            for game_data in serialized_data:
                image_name = game_data['game_img']
                game_data['game_img'] = get_image_url_from_s3(image_name).replace("//", "/")
                print(image_name)

            cache.set('games', serialized_data)
            return Response(serialized_data)
        else:
            g = Game.objects.get(pk=pk)
            serializer = GameSerializer(g)
            serialized_data = serializer.data
            image_name = serialized_data['game_img']
            serialized_data['game_img'] = get_image_url_from_s3(image_name).replace("//", "/")
            return Response(serialized_data)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
def game(request, pk=None):
    """"The function allows you to access and manage all users.
    You have the option to delete a user or promote them to a super user."""
    if request.method == 'GET':
        if pk is None:
            g = Game.objects.all()
            serializer = GameSerializer(g, many=True)
            return Response(serializer.data)
        else:
            g = Game.objects.get(pk=pk)
            serializer = GameSerializer(g)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            cache.delete('games')
            uploader = UserProfile.objects.get(user=request.user)
            game_img = request.FILES.get('game_img')
            if game_img:
                file_name = game_img.name
                presigned_url = generate_presigned_url(f"images/{file_name}")
                if presigned_url:
                    success = upload_file_to_s3(presigned_url, game_img)
                    if success:
                        serializer.save(uploader=uploader)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        error_message = "Error uploading game file to S3"
            else:
                serializer.save(uploader=uploader)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error_message = serializer.errors
            print(f"Error adding game: {error_message}")
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if pk is not None:
            g = Game.objects.get(pk=pk)
            serializer = GameSerializer(g, data=request.data)
            if serializer.is_valid():
                cache.delete('games')
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Please provide a valid ID."}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if pk is not None:
            g = Game.objects.get(pk=pk)
            g.delete()
            cache.delete('games')
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Please provide a valid ID."}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def signup(request):
    """ Get data from request """
    username = request.data.get("username", None)
    password = request.data.get("password", None)
    email = request.data.get("email", None)
    location = request.data.get('location', None)
    age = request.data.get('age', None)
    phone = request.data.get('phone', None)
    phonecontact = request.data.get('phonecontact', None)
    emailcontact = request.data.get('emailcontact', None)
    webcontact = request.data.get('webcontact', None)

    if not username or not password:
        return Response({'error': 'Missing required fields'}, status=400)

    try:
        user = User.objects.create_user(username=username, password=password, email=email)
    except IntegrityError:
        return Response({'error': 'Username already exists'}, status=400)

    user_profile = UserProfile.objects.create(
        user=user,
        location=location,
        age=age,
        phone=phone,
        email=email,
        phonecontact=phonecontact,
        emailcontact=emailcontact,
        webcontact=webcontact
    )

    token, created = Token.objects.get_or_create(user=user)

    data = {
        "message": f"New user created with ID: {user.id}",
        "token": token.key,
        'username': username,
        "user": {
            "id": user_profile.id,
            "username": username,
            "profile": {
                "location": location,
                "age": age,
                "phone": phone,
                "email": email,
                "phonecontact": phonecontact,
                "emailcontact": emailcontact,
                "webcontact": webcontact,
            }
        }
    }
    return Response(data, status=201)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def inbox(request, pk=None):
    """The function retrieves the inbox for the superuser, containing messages sent by users.
      It displays the messages, allowing you to delete them and edit their status as 'completed' or 'in progress'."""
    if request.method == 'GET':
        if pk is not None:
            try:
                note = ContactMsg.objects.get(pk=pk)
                serializer = ContactMsgSerializer(note)
                return Response(serializer.data)
            except ContactMsg.DoesNotExist:
                return Response({'error': 'Message not found.'}, status=404)
        else:
            notes = ContactMsg.objects.all()
            serializer = ContactMsgSerializer(notes, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['status'] = 'in_progress'  # Set the status to 'In Progress'
        serializer = ContactMsgSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'PATCH':
        if pk is not None:
            try:
                note = ContactMsg.objects.get(pk=pk)
                note.status = 'completed'
                note.save()
                serializer = ContactMsgSerializer(note)
                return Response(serializer.data)
            except ContactMsg.DoesNotExist:
                return Response({'error': 'Message not found.'}, status=404)
        else:
            return Response({'error': 'Message ID (pk) is required for marking as completed.'}, status=400)

    elif request.method == 'DELETE':
        if pk is not None:
            try:
                note = ContactMsg.objects.get(pk=pk)
                note.delete()
                return Response({'message': 'Message deleted successfully.'}, status=200)
            except ContactMsg.DoesNotExist:
                return Response({'error': 'Message not found.'}, status=404)
        else:
            return Response({'error': 'Message ID (pk) is required for deletion.'}, status=400)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_inbox(request, pk):
    """The function retrieves the user's inbox where they receive messages from other users regarding the games they would like to buy.
      It allows the user to read the messages and delete them if needed."""
    if request.method == 'GET':
        try:
            user_profile = UserProfile.objects.get(pk=pk)
            user_id = user_profile.user.id
            messages = user_profile.user.received_messages.all()
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile does not exist'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        request.data['recipient'] = pk  # Set the recipient ID in the request data
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return Response({'error': 'Message does not exist'}, status=status.HTTP_404_NOT_FOUND)
        message.is_read = True
        message.save()
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        if pk is not None:
            try:
                message = Message.objects.get(pk=pk)
                message.delete()
                return Response({'message': 'Message deleted successfully.'}, status=200)
            except Message.DoesNotExist:
                return Response({'error': 'Message not found.'}, status=404)
        else:
            return Response({'error': 'Message ID (pk) is required for deletion.'}, status=400)


@api_view(['GET'])
def serve_game_pagination(request):
    page_size = int(request.GET.get('page_size', 20))
    page = int(request.GET.get('page_num', 0))

    start = page * page_size
    end = start + page_size

    game = Game.objects.filter(id__range=[start, end-1])

    game_data = GameSerializer(game, many=True).data

    res = {'data': game_data,
           'next_page':page + 1,
           'hes_more': end <= len(game)
           }
    return Response(res)


def chat(req):
    return render(request=req, template_name='my_app/index.html')


def serve_chat_rooms(request):
    """The function retrieves the chat room, allowing users to engage in real-time conversation and communication."""
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    groups = list(channel_layer.groups.keys())
    return JsonResponse({'chat_rooms': groups})


def serve_room_participants(request, group):
    """The function retrieves the list of participants in a chat room,
      providing information about the users currently present in the room."""
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    participants = list(channel_layer.groups.get(group, []))
    return JsonResponse({'room_participants': participants})
