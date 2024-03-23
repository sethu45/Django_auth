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

# def index(request):
#     if request.user.is_authenticated:
#         return render(request, 'home.html')  # Render home page for normal users
#     else:
#         return redirect('login')  # Redirect unauthenticated users to login page


from django.contrib.auth.decorators import login_required
def index(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            # Get all registered users
            users = Account.objects.all().order_by('username')
            context = {'users': users}
        else:
            context = {'username': request.user.username}
        return render(request, 'home.html', context)
    else:
        return redirect('login')

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


# class UserDashboardView(APIView):
#   permission_classes = [IsAuthenticated]

#   def get(self, request):
#     print("Dashboard view accessed.")
#     if request.user.is_authenticated:
#       print("User is authenticated.")
#       if request.user.is_superuser:
#         users = Account.objects.all()
#         serializer = RegistrationSerializer(users, many=True)
#         print(users)
#         return Response(serializer.data)
#       else:
#         return Response({'message': f"Welcome, {request.user.username}"})
#     else:
#       print("User is not authenticated.")
#       return Response(status=401)  # Unauthorized
