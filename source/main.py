import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Cargar el conjunto de datos de imágenes
train_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
    'images',
    target_size=(64, 64),
    batch_size=32,
    class_mode='binary'
)

# Construir el modelo
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compilar el modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Entrenar el modelo
model.fit(train_generator, epochs=10)

# Función para predecir si una persona tiene mucha ropa o no
def predict_clothing(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (64, 64))
    image = np.expand_dims(image, axis=0)
    prediction = model.predict(image)[0][0]
    if prediction > 0.5:
        return "Mucha ropa"
    else:
        return "Poca ropa"

# Ejemplo de uso
image_path = 'prueba.jpg'
result = predict_clothing(image_path)
print(result)
