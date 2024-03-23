from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, AccountAuthenticationForm
# from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from account.models import Account
from .api.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from account.api.authentication import *


def index(request):
    return render(request, 'home.html')


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'register.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, "login.html", context)


class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.is_superuser:  # Check if user is admin
            users = Account.objects.all()
            serializer = RegistrationSerializer(data=request.user)
            print(serializer)
            data = {}
            if serializer.is_valid():

                for user in serializer.validated_data:
                    data['user'] = user.username
                token, _ = Token.objects.get_or_create(user=users)
                is_expired, token = token_expire_handler(token)
                data['token'] = token
            # if serializer.is_valid():
            #     data[users]
            print(data)
            # {'user_list': user_list}
            return render(request, 'home.html', context=data)
        else:
            return Response({"message": f"Welcome, {request.user.username}"})
