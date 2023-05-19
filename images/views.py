import os
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

def view_images(request):
    if request.user.is_authenticated:
        user_folder = os.path.join(settings.MEDIA_ROOT, request.user.username)
        images = []
        if os.path.exists(user_folder):
            files = os.listdir(user_folder)
            images = [settings.MEDIA_URL+"/".join([request.user.username, f]) for f in files if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))]
            return render(request, "images/view_images.html", {"images": images})
    return redirect(reverse('login'))

def view_image(request, image_id):
    if request.user.is_authenticated:
        user_folder = os.path.join(settings.MEDIA_ROOT, request.user.username)
        if os.path.exists(user_folder):
            image_name = f"{image_id}.jpg"
            for file_name in os.listdir(user_folder):
                if file_name == image_name:
                    image_path = settings.MEDIA_URL+"/".join([request.user.username, f"{image_id}.jpg"])
                    print(image_path)
                    break
                else:
                    image_path = ""
            return render(request, "images/view_image.html", {"image": image_path})

    return redirect(reverse('login'))

def delete_image(request):
    image_path = request.POST.get('image_name', '')
    user_folder = os.path.join(settings.MEDIA_ROOT, request.user.username)
    image_name = os.path.basename(image_path)
    full_path = os.path.join(user_folder,image_name)
    try:
        os.remove(full_path)
        print(f"Image deleted: {full_path}")
    except OSError as e:
        print(f"Error deleting image: {e}")
    return view_images(request)
    

