from keras.models import load_model
import numpy as np
from PIL import Image, ImageOps
import requests
import tensorflow as tf

with open('Api/models/labels.txt', 'r') as file:
    class_labels = [line.strip() for line in file.readlines()]

#custom prediction
def load_and_prep_image(filepath, image_size):
    img = tf.io.read_file(filepath) #read image

    img = tf.io.decode_image(img,channels=3) 
    # img = tf.image.decode_image(img) # decode the image to a tensor
    img = tf.image.resize(img, size = [image_size, image_size]) # resize the image
    img = img/255. # rescale the image
    return img

def classify_image(filepath, model_path, image_size=229, class_labels=class_labels):
    # loading trained model
    trained_model=load_model(model_path, compile=False)
    trained_model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )

    # Import the target image and preprocess it
    img = load_and_prep_image(filepath, image_size)

    prediction = trained_model.predict(tf.expand_dims(img, axis=0))
    index = np.argmax(prediction)

    class_name = class_labels[index]
    confidence_score = prediction[0][index]

    return {
        "idx" : index,
        'class' : class_name,
        'score' : f'{confidence_score*100:02.2f}%'
    }

#google teachable machine
def predict_class(filepath, model_path, image_size = 299):
    np.set_printoptions(suppress=True)

    model = load_model(model_path ,compile=False)
    model.compile(
        loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )

    data = np.ndarray(shape=(1, image_size, image_size, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(filepath).convert("RGB")

    # resizing the image to be at least 299 X 299 and then cropping from the center
    size = (image_size, image_size)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_labels[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    # print("Class:", class_name[2:], end=" \n")
    # print("Confidence Score:", confidence_score)

    result = {
        "idx" : index,
        "class" : class_name,
        "score" :f'{(confidence_score*100):2.2f}%'
    }

    return result

# using bytes
def prepare_image(image, image_size):
    image = tf.image.decode_jpeg(image, channels=3)

    image = tf.cast(image, tf.float32)
    image /= 255.0
    image = tf.image.resize(image, [image_size, image_size])

    image = np.expand_dims(image, axis=0)

    return image

def classify_using_bytes(image_bytes, model_path, image_size):
    model = load_model(model_path, compile=False)
    model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )

    prediction = model.predict(prepare_image(image_bytes, image_size))
    index = np.argmax(prediction, axis=1)[0]

    class_name = class_labels[index]
    confidence_score = prediction[0][index]

    return {
        'idx' : index,
        'class' : class_name,
        'score' : f'{confidence_score*100:02.2f}%'
    }

def classify_using_url(url, model_path, image_size=299):
    image_source = requests.get(url).content
    
    return classify_using_bytes(image_source, model_path, image_size)

if __name__ == '__main__':
    result = classify_image('Api/test1.jpeg', 'Api/models/model.h5', image_size=224)
    idx = result.get('idx')
    print(result)


    