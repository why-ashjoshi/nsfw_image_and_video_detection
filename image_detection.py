from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the pre-trained NSFW MobileNet model without compiling it
model = load_model(r'C:\Users\INTEL\Desktop\thh\models\nsfw_mobilenet2.224x224.h5', compile=False)

def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize the image array
    return img_array

def detect_nudity(image_path):
    img_array = preprocess_image(image_path)
    prediction = model.predict(img_array)
    
    # Assuming the model outputs a binary classification:
    nsfw_score = prediction[0][1]  # Probability of being NSFW
    return nsfw_score

def is_nsfw(nsfw_score, threshold=0.04):
    return nsfw_score > threshold
