import os
import shutil

# Carpeta principal donde están todas las subcarpetas con imágenes
carpeta_principal = r"C:/Users/anais/OneDrive/Escritorio/TareaIA/InteligenciArtificial/Animales/turtles-data/data/images"

# Carpeta donde se guardarán todas las imágenes
carpeta_destino = r"C:/Users/anais/OneDrive/Escritorio/TareaIA/InteligenciArtificial/Animales/tortugas2"
os.makedirs(carpeta_destino, exist_ok=True)

# Extensiones de imágenes
extensiones_imagenes = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]

# Recorrer todas las subcarpetas
for carpeta_raiz, subcarpetas, archivos in os.walk(carpeta_principal):
    for archivo in archivos:
        nombre_archivo, extension = os.path.splitext(archivo)
        if extension.lower() in extensiones_imagenes:
            ruta_origen = os.path.join(carpeta_raiz, archivo)
            ruta_destino = os.path.join(carpeta_destino, archivo)

            # Evitar sobrescribir archivos con el mismo nombre
            contador = 1
            while os.path.exists(ruta_destino):
                ruta_destino = os.path.join(carpeta_destino, f"{nombre_archivo}_{contador}{extension}")
                contador += 1

            shutil.copy2(ruta_origen, ruta_destino)

print("¡Todas las imágenes se han copiado a la carpeta destino!")
