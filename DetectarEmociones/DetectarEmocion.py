import cv2 as cv
import os

# === Cargar modelo entrenado ===
faceRecognizer = cv.face.LBPHFaceRecognizer_create()
faceRecognizer.read('Emociones.yml')

# === Etiquetas (orden según las carpetas del entrenamiento) ===
emociones = ['Enojado', 'Feliz', 'Triste']

# === Cargar detector de rostros ===
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')

# === Activar cámara ===
cap = cv.VideoCapture(0)

print("🎥 Iniciando reconocimiento de emociones... (Presiona ESC para salir)")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in rostros:
        # Recortar el rostro detectado
        rostro_img = gray[y:y+h, x:x+w]
        rostro_img = cv.resize(rostro_img, (100, 100), interpolation=cv.INTER_CUBIC)
        rostro_img = cv.equalizeHist(rostro_img)

        # Predicción del modelo
        result = faceRecognizer.predict(rostro_img)
        prediccion = emociones[result[0]]
        distancia = result[1]

        # Mostrar en consola (opcional, útil para ajustar umbral)
        print(f"Emoción: {prediccion}, Distancia: {distancia}")

        # Dibujar recuadro y texto en pantalla
        if distancia < 100:
            color = (0, 255, 0)
            texto = prediccion
        else:
            color = (0, 0, 255)
            texto = "Desconocido"

        cv.putText(frame, f"{texto} ({int(distancia)})", (x, y - 10), 2, 0.9, color, 2, cv.LINE_AA)
        cv.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    # Mostrar video en ventana
    cv.imshow('Reconocimiento de Emociones', frame)

    # Salir con ESC
    k = cv.waitKey(1)
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()
print("🧠 Reconocimiento finalizado.")

