import os
from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings

def view_images(request):
    if request.user.is_authenticated:
        user_folder = os.path.join(settings.MEDIA_ROOT, request.user.username)
        images = []
        if os.path.exists(user_folder):
            files = os.listdir(user_folder)
            images = [settings.MEDIA_URL+"/".join([request.user.username, f]) for f in files if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))]
            print(images)
            return render(request, "images/view_images.html", {"images": images})
    return redirect(reverse('login'))