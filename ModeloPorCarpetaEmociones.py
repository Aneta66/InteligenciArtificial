import cv2 as cv
import numpy as np
import os

dataSet = 'C:/Users/anais/OneDrive/Escritorio/TareaIA/InteligenciArtificial/Emociones'

for emo in ['enojado', 'feliz', 'triste']:
    print(f"\n🔹 Entrenando modelo para '{emo}'...")
    path = os.path.join(dataSet, emo)
    imgs = []
    labels = []

    # Verifica si la carpeta existe
    if not os.path.exists(path):
        print(f"⚠️ La carpeta '{path}' no existe, se omite.")
        continue

    archivos = os.listdir(path)
    print(f"📁 Carpeta: {path}")
    print(f"📸 Total de imágenes encontradas: {len(archivos)}")

    for i, fname in enumerate(archivos):
        img_path = os.path.join(path, fname)
        img = cv.imread(img_path, 0)
        if img is not None:
            img = cv.resize(img, (100, 100))
            img = cv.equalizeHist(img)
            imgs.append(img)
            labels.append(0)

        # Muestra progreso cada 500 imágenes
        if (i + 1) % 500 == 0:
            print(f"   🧠 Procesadas {i + 1}/{len(archivos)} imágenes de '{emo}'")

    print(f"✅ Total procesadas: {len(imgs)} imágenes para '{emo}'")

    recog = cv.face.LBPHFaceRecognizer_create()
    recog.train(imgs, np.array(labels))
    recog.write(f'{emo}.xml')
    print(f"💾 Modelo '{emo}.xml' guardado correctamente.")
