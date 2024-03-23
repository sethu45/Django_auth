from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from account.models import Account
from account.api.serializers import RegistrationSerializer
from account.api.authentication import *
# from rest_framework.authtoken.models import token_expire_handler, expires_in
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)
from django.shortcuts import render


@api_view(['POST', ])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = account.email
            data['username'] = account.username
            # token = Token.objects.get(user=account).key
            # data['token'] = token
            token, _ = Token.objects.get_or_create(user=account)
            is_expired, token = token_expire_handler(token)
            data['token'] = token.key
            data['token_is_expired'] = is_expired
        else:
            data = serializer.errors
        return Response(data)


@api_view(["GET"])
def user_info(request):
    return Response({
        'user': request.user.username,
        'expires_in': expires_in(request.auth)
    }, status=HTTP_200_OK)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def admin_users_view(request):
#     if request.user.is_staff:
#         users = Account.objects.all()  # Assuming UserProfile model for user details
#         serializer = RegistrationSerializer(users, many=True)
#         return render(request, 'admin_users.html', {'users': serializer.data})
#     else:
#         return Response({"error": "You don't have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def normal_user_welcome_view(request):
#     return render(request, 'normal_user.html', {'username': request.user.username})
