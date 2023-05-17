import io
import os
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import CustomUserForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from datetime import datetime
import keras
from PIL import Image
import numpy as np
import cv2

IMG_SIZE = 50
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
MODEL_FILEPATH = os.path.join(MODEL_DIR, 'old_my_model.h5')
print(MODEL_FILEPATH)
model = keras.models.load_model(MODEL_FILEPATH)
my_dict = { 0:'а', 1:'ә', 2:'з', 3:'и', 4:'і', 5:'й', 
            6:'к', 7:'қ', 8:'л', 9:'м', 10:'н', 11:'ң',
            12:'б', 13:'о', 14:'ө', 15:'п', 16:'р', 17:'с',
            18:'т', 19:'у', 20:'ү', 21:'ұ', 22:'ф', 23:'в',
            24:'х', 25:'һ', 26:'ц', 27:'ч', 28:'ш', 29:'щ',
            30:'ъ', 31:'ы', 32:'ь', 33:'э', 34:'г', 35:'ю',
            36:'я', 37:'ғ', 38:'д', 39:'е', 40:'ё', 41:'ж'}
# my_dict = { 0:'а', 1:'ә', 2:'з', 3:'и', 4:'й', 5:'к', 
#             6:'қ', 7:'л', 8:'м', 9:'н', 10:'ң', 11:'о',
#             12:'б', 13:'ө', 14:'п', 15:'р', 16:'с', 17:'т',
#             18:'у', 19:'ұ', 20:'ү', 21:'ф', 22:'х', 23:'в',
#             24:'ц', 25:'ч', 26:'ш', 27:'щ', 28:'һ', 29:'ъ',
#             30:'ы', 31:'і', 32:'ь', 33:'э', 34:'г', 35:'ю',
#             36:'я', 37:'ғ', 38:'д', 39:'е', 40:'ё', 41:'ж'}

def segment_character(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform binary thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Find contours of characters
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours from left to right
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

    # Extract character images from contours
    character_images = []
    for contour in contours:
        # Get bounding box of contour
        x, y, w, h = cv2.boundingRect(contour)

        # Expand the bounding box by 4 pixels in each direction
        x -= 4
        y -= 4
        w += 8
        h += 8

        # Ensure the expanded bounding box is within the image boundaries
        x = max(0, x)
        y = max(0, y)
        w = min(w, image.shape[1] - x)
        h = min(h, image.shape[0] - y)

        # Extract character image and resize to 28x28
        character_image = gray[y:y+h, x:x+w]
        character_image = cv2.resize(character_image, (IMG_SIZE, IMG_SIZE))

        # Append character image to list
        character_images.append(character_image)

    return character_images

def predict_canvas(request):
    if request.method == "POST" and request.FILES.get("image"):
        image_file = request.FILES.get("image")
        image_data = image_file.read()
        pil_image = Image.open(io.BytesIO(image_data))
        image = np.array(pil_image)
        # print(type(image))

        chars = segment_character(image)
        predicted_characters = []
        for char in chars:
            char = char.reshape((1, IMG_SIZE, IMG_SIZE, 1))
            char = char / 255.0
            prediction = model.predict(char)

         # Resize and grayscale image
            # resized_image = cv2.resize(char, (IMG_SIZE, IMG_SIZE))
            # gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

            # img_array = np.array(gray_image)
            # img_array = img_array / 255.0
            # img_array = np.expand_dims(img_array, axis=0)

            # prediction = model.predict(img_array)

            prediction_class = np.argmax(prediction)
            prediction_class = int(prediction_class)
            
            # print(prediction_class)

            predicted_character = my_dict[prediction_class]
            predicted_characters.append(predicted_character)
            predicted_word = ''.join(predicted_characters)
        return JsonResponse({'prediction': predicted_word}) 
    return JsonResponse({"prediction": False})

def index(request):
    data = {
        'title':'Handwritten Kazakh Language word recognition',
        'values':['Some', 'Hello', '123']
    }
    return render(request, 'main/index.html', data)

def about(request):
    return render(request, 'main/about.html')

def save_canvas(request):
    if request.method == "POST" and request.FILES.get("image"):
        image_file = request.FILES["image"]
        user = request.user
        # filename = "sketch.png"  # or use a unique filename based on user, date, etc.
        if user.is_authenticated:
            # create a folder for the user if it doesn't exist
            user_folder = os.path.join(settings.MEDIA_ROOT, user.username)
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)
            # generate a unique filename
            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            filename = f"{timestamp}_{image_file.name}"
            # save the image in the user's folder
            with open(os.path.join(user_folder, filename), "wb") as f:
                f.write(image_file.read())
            return JsonResponse({"success": True, "filename": os.path.join(user.username, filename)})
    return JsonResponse({"success": False})


def home(request):
    return redirect('view_images')

def signup(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserForm()
    return render(request, 'main/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = '/'

@login_required
def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'main/profile.html', context)

