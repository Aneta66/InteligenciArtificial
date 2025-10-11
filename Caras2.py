import cv2 as cv
import os

# Clasificador de rostros
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')

# Usar la cámara (0 = cámara predeterminada)
cap = cv.VideoCapture(0)


i = 0  

# Carpeta donde se guardarán los rostros
output_dir = "C:/Users/anais/OneDrive/Escritorio/TareaIA/InteligenciArtificial/Anita"
os.makedirs(output_dir, exist_ok=True)

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ No se pudo acceder a la cámara.")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in rostros:
        # Dibujar rectángulo en el rostro
        cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)

        # Recortar el rostro detectado
        frame2 = frame[y:y+h, x:x+w]
        frame2 = cv.resize(frame2, (100, 100), interpolation=cv.INTER_AREA)

        # Guardar cada 10 frames
        if i % 10 == 0:
            filename = os.path.join(output_dir, f"rostro_{i}.jpg")
            cv.imwrite(filename, frame2)
            cv.imshow('Rostro detectado', frame2)

    # Mostrar la cámara en tiempo real
    cv.imshow('Camara - Detección de Rostros', frame)

    i += 1
    k = cv.waitKey(1)
    if k == 27:  # Tecla ESC para salir
        break

cap.release()
cv.destroyAllWindows()
