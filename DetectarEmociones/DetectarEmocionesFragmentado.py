import cv2 as cv
import numpy as np
from collections import deque #corriendo el CNN , carpeta de jupyter , cnn y el data set en dobox(nose como se escribe) 8 clases
#modificar lo que vamos a clasificar , que clasifique bien

# ==== CONFIGURACIÓN INICIAL ====
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')

# Cargar los tres modelos entrenados
modelos = {
    'feliz': cv.face.LBPHFaceRecognizer_create(),
    'triste': cv.face.LBPHFaceRecognizer_create(),
    'enojado': cv.face.LBPHFaceRecognizer_create()
}

modelos['feliz'].read('feliz.xml')
modelos['triste'].read('triste.xml')
modelos['enojado'].read('enojado.xml')

print("✅ Modelos cargados correctamente")

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("❌ No se pudo abrir la cámara.")
    exit()

# ==== HISTORIAL DE PREDICCIONES ====
# Guarda las últimas N emociones detectadas (para suavizar el resultado)
historial = deque(maxlen=10)

# ==== BUCLE PRINCIPAL ====
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in rostros:
        rostroROI = gray[y:y+h, x:x+w]
        rostroROI = cv.resize(rostroROI, (100, 100), interpolation=cv.INTER_CUBIC)
        rostroROI = cv.equalizeHist(rostroROI)

        emociones_resultados = {}
        for emo, modelo in modelos.items():
            label, distancia = modelo.predict(rostroROI)
            emociones_resultados[emo] = distancia

        # Selecciona la emoción con menor distancia
        emocion_predicha = min(emociones_resultados, key=emociones_resultados.get)
        confianza = emociones_resultados[emocion_predicha]

        # Guarda la emoción detectada en el historial
        historial.append(emocion_predicha)

        # Calcula la emoción más común en el historial
        emocion_estable = max(set(historial), key=historial.count)

        # Dibuja en pantalla
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        texto = f"{emocion_estable} ({confianza:.2f})"
        cv.putText(frame, texto, (x, y - 10),
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        print(f"→ Detección instantánea: {emocion_predicha} ({confianza:.2f}) | Promedio: {emocion_estable}")

    cv.imshow('Detector de Emociones (Suave)', frame)

    k = cv.waitKey(1)
    if k == 27:  # tecla ESC
        break

cap.release()
cv.destroyAllWindows()
