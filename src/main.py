import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models
from torch.utils.data import DataLoader, random_split
from PIL import Image

# 1. Preparar los datos

# Directorio que contiene las imágenes
data_dir = './imagenes_entrenamiento'

# Tamaño de los lotes de datos
batch_size = 8

# Transformaciones que se aplican a las imágenes
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Redimensionar las imágenes a 224x224 píxeles
    transforms.ToTensor(),  # Convertir las imágenes a tensores
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # Normalizar los colores
])

# Cargar las imágenes y asignar etiquetas automáticamente según los nombres de las carpetas
dataset = datasets.ImageFolder(data_dir, transform=transform)

# Dividir el conjunto de datos en entrenamiento y validación
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

# Crear cargadores de datos para el entrenamiento y la validación
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

# 2. Entrenar el modelo

# Utilizar ResNet-18 preentrenada
model = models.resnet18(pretrained=True)

# Modificar la capa final para clasificar en 3 clases
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 3)

# Definir la función de pérdida y el optimizador
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Número de épocas de entrenamiento
num_epochs = 5
for epoch in range(num_epochs):
    model.train()  # Establecer el modo de entrenamiento
    running_loss = 0.0
    for inputs, labels in train_loader:  # Iterar sobre los lotes de datos
        optimizer.zero_grad()  # Limpiar los gradientes
        outputs = model(inputs)  # Hacer la predicción
        loss = criterion(outputs, labels)  # Calcular la pérdida
        loss.backward()  # Propagar hacia atrás
        optimizer.step()  # Actualizar los parámetros
        running_loss += loss.item()
    print(f"Época [{epoch+1}/{num_epochs}], Pérdida: {running_loss/len(train_loader):.4f}")

# 3. Evaluar el modelo

model.eval()  # Establecer el modo de evaluación
correct = 0
total = 0
with torch.no_grad():  # Desactivar el cálculo de gradientes
    for inputs, labels in val_loader:  # Iterar sobre los lotes de datos de validación
        outputs = model(inputs)
        _, predicted = torch.max(outputs, 1)  # Obtener la clase con la mayor probabilidad
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
print(f'Exactitud de validación: {100 * correct / total:.2f}%')

# 4. Hacer predicciones

def predict_image(image_path):
    """Función para predecir la clase de una imagen."""
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)  # Aplicar las transformaciones y añadir dimensión de lote
    model.eval()
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
    classes = dataset.classes
    return classes[predicted.item()]

# Predecir la clase de la imagen 'prueba.png'
result = predict_image('./imagenes_prueba/prueba1.jpg')
print(f'La persona en la imagen "prueba1.jpg" tiene "{result}" ropa.')
