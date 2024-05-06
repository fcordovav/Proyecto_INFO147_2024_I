import os

def contar_imagenes(ruta_carpeta):
    os.chdir(ruta_carpeta)
    cantidad_imagenes = 0
    # Recorre todos los archivos en la carpeta
    for archivo in os.listdir():
        # Verifica si el archivo es una imagen según el sistema operativo
        if os.path.isfile(archivo) and any(archivo.lower().endswith(ext) for ext in (".jpg", ".avif", ".png", ".webp")):
            cantidad_imagenes += 1
    
    return cantidad_imagenes

# Ruta de la carpeta donde se encuentran las imágenes
ruta_carpeta_imagenes = "./imagenes_entrenamiento/mucha"

# Llama a la función contar_imagenes y muestra el resultado
cantidad_total_imagenes = contar_imagenes(ruta_carpeta_imagenes)
print("Cantidad total de imágenes en la carpeta:", cantidad_total_imagenes)
