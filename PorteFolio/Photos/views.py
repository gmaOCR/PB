import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from Profiles.models import CustomUser
from .forms import PhotoForm, DeleteForm
from .models import Photo


@login_required
def add_photo(request):
    if request.method == 'POST':
        print("Soumission du formulaire POST")
        photo_form = PhotoForm(request.POST, request.FILES)
        if photo_form.is_valid():
            print("Le formulaire est valide")
            photo = photo_form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('home')
    else:
        print("Affichage du formulaire GET")
        photo_form = PhotoForm()
    return render(request, 'add_photo.html', {'photo_form': photo_form})


@login_required
def edit_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    edit_form = PhotoForm(instance=photo)

    if request.method == 'POST':
        if 'delete_media' in request.POST:
            if photo.thumbnail:
                thumbnail_path = photo.thumbnail.path
                os.remove(thumbnail_path)
                photo.thumbnail = None

            if photo.image:
                image_path = photo.image.path
                os.remove(image_path)
                photo.image = None

            if photo.thumbnail or photo.image:
                photo.save()
                messages.success(request, "La miniature et l'image ont été supprimées avec succès.")

        if 'edit_photo' in request.POST:
            edit_form = PhotoForm(request.POST, files=request.FILES, instance=photo)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, "La photo a été correctement modifiée.")
                return redirect('home')

    context = {
        'edit_form': edit_form,
        'photo': photo,
    }
    return render(request, 'edit_photo.html', context=context)


@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    if request.method == 'POST':
        photo.delete()
        return redirect('home')

    return render(request, 'delete_photo.html', context={'photo': photo})


@login_required
def home(request):
    photos = Photo.objects.all()
    users = CustomUser.objects.all()
    context = {
        'photos': photos,
        'users': users,
    }
    return render(request, 'home.html', context)
