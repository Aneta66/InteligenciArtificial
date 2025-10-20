# Entrenamiento del modelo de reconocimiento de emociones
# usando LBPH (Local Binary Patterns Histogram)

import cv2 as cv
import numpy as np
import os
import time

# === RUTA DE TU DATASET ===
dataSet = 'C:/Users/anais/OneDrive/Escritorio/TareaIA/InteligenciArtificial/Emociones'
# En Ubuntu sería algo como:
# dataSet = '/home/usuario/Emociones'

# === INICIO DEL ENTRENAMIENTO ===
inicio = time.time()
emociones = os.listdir(dataSet)
print("📁 Carpetas encontradas:", emociones)

labels = []
facesData = []
label = 0
contador = 0
total = sum(len(os.listdir(os.path.join(dataSet, f))) for f in emociones)

# === LECTURA DE IMÁGENES ===
for emo in emociones:
    emoPath = os.path.join(dataSet, emo)
    print(f"\n➡ Procesando '{emo}' ({len(os.listdir(emoPath))} imágenes) Label={label}")

    for faceName in os.listdir(emoPath):
        ruta = os.path.join(emoPath, faceName)
        img = cv.imread(ruta, 0)
        if img is None:
            print(f"⚠️ No se pudo leer: {ruta}")
            continue
        img = cv.resize(img, (100,100))
        img = cv.equalizeHist(img)  # mejora contraste y uniformiza luz
        facesData.append(img)
        labels.append(label)
        contador += 1
        if contador % 200 == 0:
            print(f"  Procesadas {contador}/{total} imágenes...")

    label += 1

print(f"\n✅ Total de imágenes procesadas: {contador}")
print("🕒 Tiempo de carga:", round(time.time() - inicio, 2), "segundos")

# === ENTRENAMIENTO LBPH ===
print("\n🚀 Iniciando entrenamiento...")
t0 = time.time()
faceRecognizer = cv.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
faceRecognizer.train(facesData, np.array(labels))
t1 = time.time()

print("✅ Entrenamiento completado en", round(t1 - t0, 2), "segundos.")
faceRecognizer.write('Emociones.yml')
print("💾 Modelo guardado como Emociones.yml")
