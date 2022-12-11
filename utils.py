import os
import cv2
import time
import json
import threading
import numpy as np
import face_recognition

from datetime import datetime, timedelta


class Camera(object):
    def __init__(self, src=0):
        print("loading...")
        start_time = time.perf_counter()
        self.capture = cv2.VideoCapture(src)
        print("Camera loaded! in", time.perf_counter()-start_time)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
       
        self.FPS = 1/30
        self.FPS_MS = int(self.FPS * 1000)
        
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        
    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            time.sleep(self.FPS)
    
    def show_frame(self, img):
        cv2.imshow('Camera', img)
        cv2.waitKey(self.FPS_MS)


class Recognizer:
    def __init__(self, foto_folder_path: str, event):
        self.names = []
        self.images = []
        self.encoded_images = []
        self.camera = None
        self.path = foto_folder_path
        self.GREEN = (0, 255, 255)
        self.BLUE = (243, 255, 71)
        
        self.CURRENT_COLOR = self.BLUE

        self.load_images()
        self.find_encoding()
        self.event = event
        
        # SHU KOD YANGI RASMLARNI PAPKASINI OCHADI
        # KECHAGI PAPKANI O'CHIRIB YUBORADI
        self.today = datetime.now()
        self.yesterday = (self.today - timedelta(days=1)).strftime('%Y_%m_%d')
        self.today = self.today.strftime('%Y_%m_%d')
        
        self.yesterday_folder = os.path.join('data', self.yesterday)
        self.today_folder = os.path.join('data', self.today)

        if os.path.exists(self.yesterday_folder):
            os.system(f"rmdir /s /q {self.yesterday_folder} /s")

        if not os.path.exists(self.today_folder):
            os.mkdir(self.today_folder)
        #----------------------------------------

    def start(self, camera):
        print('Calling start')
        self.event.clear()
        print('event clear')
        self.camera = camera
        print('load camera')
        while not self.event.is_set():
            self.start_recognizing()

    def stop(self):
        print('Calling stop')
        self.event.set()
        # cv2.destroyAllWindows()

    def find_encoding(self):
        self.encoded_images = []

        for img in self.images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            self.encoded_images.append(encode)

    def load_images(self):
        path_list_of_images = os.listdir(self.path)
        for p in path_list_of_images:
            img = cv2.imread(f'{self.path}/{p}')
            self.images.append(img)
            self.names.append(os.path.splitext(p)[0])            

    def save_today_face(self, name, img):
        cv2.imwrite(os.path.join(self.today_folder,name+'.jpg'), img)

    def make_attendance(self, name: str):
        today_file =  os.path.join(self.today_folder, self.today+'.json')

        if not os.path.exists(today_file):
            with open(today_file, 'w') as f:
                f.write(json.dumps({name: True}))
                return
        
        with open(today_file, 'r') as f:
            data = json.loads(f.read())
            if data.get(name, None):
                return True
            data[name] = True

        with open(today_file, 'w') as f:
            f.write(json.dumps(data, indent=4))

    def make_rectangle(self, img, name, face_location):
        y1, x2, y2, x1  = face_location
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1-10, y1-10), (x2+20, y2+20), self.CURRENT_COLOR, 2)
        cv2.rectangle(img, (x1-10, y2-10), (x2+20, y2+25), self.CURRENT_COLOR, cv2.FILLED)
        cv2.putText(img, name, (x1, y2+20), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 0), 2)
        return y1, x2, y2, x1

    def mark_matched_face(self, matched_face, name, img, faceLoc):
        self.save_today_face(name, img)
        if matched_face:
            y1, x2, y2, x1 = self.make_rectangle(img, name, faceLoc)
            
            if self.make_attendance(name):
                self.CURRENT_COLOR = self.GREEN
            else:
                self.CURRENT_COLOR = self.BLUE

    def start_recognizing(self):
        success, img = self.camera.capture.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(self.encoded_images, encodeFace)
            faceDis = face_recognition.face_distance(self.encoded_images, encodeFace)
            matchIndex = np.argmin(faceDis)
            name = self.names[matchIndex].upper()
            self.mark_matched_face(matches[matchIndex], name, img, faceLoc)

        self.camera.show_frame(img)
