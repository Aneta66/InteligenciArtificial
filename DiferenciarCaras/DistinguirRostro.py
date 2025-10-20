import cv2 as cv
import os 

faceRecognizer = cv.face.LBPHFaceRecognizer_create()
faceRecognizer.read('LBPH.xml')
faces =['Anita', 'Balu', 'Kevin', 'Missa', 'Yiseni']
cap = cv.VideoCapture(0)
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
while True:
    ret, frame = cap.read()
    if ret == False: break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cpGray = gray.copy()
    rostros = rostro.detectMultiScale(gray, 1.1, 5)
    for(x, y, w, h) in rostros:
        frame2 = cpGray[y:y+h, x:x+w]
        frame2 = cv.resize(frame2,  (100,100), interpolation=cv.INTER_CUBIC)
        result = faceRecognizer.predict(frame2)
        cv.putText(frame, '{}'.format(result), (x,y-20), 1,3.3, (0,0,255), 1, 3)

        if result[1] < 120:  
            cv.putText(frame, '{}'.format(faces[result[0]]), (x, y - 25), 2, 1.1, (0,255,0), 1, cv.LINE_AA)
            cv.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
        else:
            cv.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0,0,255), 1, cv.LINE_AA)
            cv.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)

            cv.putText(frame, f"ID:{result[0]} Dist:{int(result[1])}", (x, y+h+20), 1, 1.2, (255,255,0), 1, cv.LINE_AA)

    cv.imshow('frame', frame)
    k = cv.waitKey(1)
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()