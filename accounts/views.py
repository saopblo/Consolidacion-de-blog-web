from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserRegisterForm, UserEditForm, AvatarForm
from .models import Avatar


def login_request(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"¡Bienvenido/a {user.username}!")
                return redirect('inicio')
        else:
            messages.error(
                request,
                "Usuario o contraseña incorrectos. Por favor intentá de nuevo."
            )
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "Has cerrado sesion correctamente")
    return redirect('inicio')


def registro_request(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "El registro ha sido exitoso, podes iniciar sesion")
            return redirect('inicio')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/registro.html', {'form': form})


@login_required
def editar_perfil(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil editado correctamente")
            return redirect('inicio')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'accounts/editar_perfil.html', {'form': form})


@login_required
def agregar_avatar(request):
    user = request.user
    avatar, created = Avatar.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=avatar)
        if form.is_valid():
            form.save()
            messages.success(request, "Avatar agregado correctamente")
            return redirect('inicio')
    else:
        form = AvatarForm(instance=avatar)

    return render(request, 'accounts/agregar_avatar.html', {'form': form})