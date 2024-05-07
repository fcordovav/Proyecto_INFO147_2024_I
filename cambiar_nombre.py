import os

def get_last_used_number():
    try:
        with open("last_used_number.txt", "r") as file:
            last_used_number = int(file.read())
    except FileNotFoundError:
        last_used_number = 0
    return last_used_number

def update_last_used_number(number):
    with open("last_used_number.txt", "w") as file:
        file.write(str(number))

def rename_files(folder_path):
    # Verificar si la carpeta existe
    if not os.path.isdir(folder_path):
        print("La carpeta especificada no existe.")
        return

    # Obtener la lista de archivos en la carpeta
    files = os.listdir(folder_path)
    # Obtener el último número utilizado
    last_used_number = get_last_used_number()

    # Recorrer cada archivo en la carpeta
    for file_name in files:
        # Construir la ruta completa del archivo
        file_path = os.path.join(folder_path, file_name)
        # Verificar si es un archivo regular
        if os.path.isfile(file_path):
            # Obtener la extensión del archivo
            _, file_ext = os.path.splitext(file_name)
            # Incrementar el contador
            last_used_number += 1
            # Construir el nuevo nombre del archivo
            new_name = str(last_used_number) + file_ext
            # Verificar si el nuevo nombre ya está en uso
            while os.path.exists(os.path.join(folder_path, new_name)):
                last_used_number += 1
                new_name = str(last_used_number) + file_ext
            # Renombrar el archivo
            os.rename(file_path, os.path.join(folder_path, new_name))

    # Actualizar el último número utilizado
    update_last_used_number(last_used_number)

    print("Todos los archivos han sido renombrados correctamente.")

# Ejemplo de uso
if __name__ == "__main__":
    folder_path = "./imagenes_entrenamiento/mucha"
    rename_files(folder_path)
