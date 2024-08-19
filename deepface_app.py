from deepface import DeepFace
import cv2
import time
import matplotlib.pyplot as plt
FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
DB_PATH = 'data_db'

BACKENDS = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe','yolov8','yunet','fastmtcnn']

def compareImg(img):
    try :
        dfs = DeepFace.find(img_path =img, 
            db_path = DB_PATH, 
            detector_backend = BACKENDS[1],
            model_name='Facenet512',
            silent = True
        )

        if len(dfs[0]['identity']) >=1:
            return dfs[0].iloc[0],True
        else :
            return '',False
    except :
        return '',False

def face_detection(frame):
    face = FACE_CASCADE.detectMultiScale(frame,1.1,4)
    
    return face

cap = cv2.VideoCapture(0) ;# 0 คือกล้องหลัก (หรือเปลี่ยนตามกล้องที่คุณใช้) 'http://10.77.19.150:8080/video'

while cap.isOpened()  :
    ret, frame = cap.read()
    face= face_detection(frame)
    x=y=w=h= 0
    for (x,y,w,h) in face :
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),thickness = 2)
        
        face_region = frame[y:y+h, x:x+w]

    res , result = compareImg(frame)
    if ( cv2.waitKey(1) and 0xFF == ord("e") ) or result:
        name = res['identity'].split('\\')[1]
        # print(name)
        cv2.putText(frame,name,(x,y+h+20),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),2)
        # cv2.imshow('window',frame)
    else :
        cv2.putText(frame,"Identify",(x,y+h+20),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),2)
        # cv2.imshow('window',frame)
    
 
    plt.figure(1); plt.clf()
    plt.imshow(frame[:,:,::-1])
    plt.pause(0.1)

cap.release()
cv2.destroyAllWindows()