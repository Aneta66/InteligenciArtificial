import cv2 as cv
faceRecognizer = cv.face.LBPHFaceRecognizer_create()
faceRecognizer.read('Emociones.yml')
faceRecognizer.write('Emociones.yml')