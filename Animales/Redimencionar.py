import cv2 as cv
import os

input_folder = 'C:/Users/anais/OneDrive/Escritorio/TareaIA/InteligenciArtificial/TestDeporte'
output_folder = 'C:/Users/anais/OneDrive/Escritorio/TareaIA/InteligenciArtificial/TestDeporte'

# Crear carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Límite de imágenes a procesar
limite = 2
contador = 0

for i, filename in enumerate(os.listdir(input_folder)):
    if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
        img_path = os.path.join(input_folder, filename)
        img = cv.imread(img_path)

        if img is not None:
            resized = cv.resize(img, (21, 28))
            cv.imwrite(os.path.join(output_folder, f'Golf_{contador}.jpg'), resized)
            contador += 1

            # Mostrar progreso cada 500 imágenes
            if contador % 2 == 0:
                print(f"🐾 Procesadas {contador} imágenes...")

            # Detener cuando llegue al límite
            if contador >= limite:
                print("✅ Se alcanzaron las 10,000 imágenes redimensionadas.")
                break

print(f"🎉 Total de imágenes procesadas: {contador}")
