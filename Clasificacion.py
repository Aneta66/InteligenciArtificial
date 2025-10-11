#https://github.com/opencv/opencv   Kaggle data sets de caras de alguien trsite , enojado o feliz 5 mil por emocion
import cv2 as cv 
import numpy as np 
import os
dataSet = 'C:/Users/anais/OneDrive/Escritorio/TareaIA/InteligenciArtificial/Rostros'
faces  = os.listdir(dataSet)
print(faces)

labels = []
facesData = []
label = 0 
for face in faces:
    facePath = dataSet+'/'+face
    for faceName in os.listdir(facePath):
        labels.append(label)
        facesData.append(cv.imread(facePath+'/'+faceName,0))
    label = label + 1
print(np.count_nonzero(np.array(labels)==0)) 

faceRecognizer = cv.face.EigenFaceRecognizer_create()
# Reemplaza EigenFaceRecognizer por LBPHFaceRecognizer
#faceRecognizer = cv.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
# No olvides cambiar el nombre del archivo XML si quieres: faceRecognizer.write('LBPH.xml')
faceRecognizer.train(facesData, np.array(labels))
faceRecognizer.write('Eigenface.xml')