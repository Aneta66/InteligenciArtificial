import numpy as np
import cv2 as cv


rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0) 

if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara. Revisa si otra aplicación la está usando.")
    exit()

x=y=h=w=0
count = 0 
img = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se puede recibir el frame. Saliendo...")
        break 
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5) 
    for(x, y, w, h) in rostros:
        frame = cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
        img = frame[y:y+h, x:x+w]
        if count % 10 == 0:
       
            name = f'C:\\Users\\anais\\OneDrive\\Escritorio\\TareaIA\\InteligenciArtificial\\Mirostro\\face_{count}.jpg'
            cv.imwrite(name, img)
            print(f"Guardado: {name}") 
        count = count + 1
    cv.imshow('Detección de Rostros', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()