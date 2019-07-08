import cv2
import os
import threading
from PIL import Image
from timeit import default_timer as timer


class RecordingThread (threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True
        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        size = (500,300)  #寬500,高300(width,height)
        self.out = cv2.VideoWriter('./static/video.avi',fourcc,15,size)
        #self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))

    def run(self):
        frmae_counter = 0
        while self.isRunning:
            ret, frame = self.cap.read()
            flipframe = cv2.flip(frame,0) #垂直翻轉
            #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            roi = flipframe[0:300, 0:500] #寬500,高300
            gray = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)               
            color = cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)  #再轉換一次灰階到彩色才會有三通到，儲存影片才能成功
            target = Image.fromarray(cv2.cvtColor(color, cv2.COLOR_BGR2RGB))
            if frmae_counter <= 30:
                if ret:
                    target.save(os.path.join('./static',str(frmae_counter) + '.jpg'))
                    frmae_counter += 1
                    self.out.write(color)
                    #self.out.write(roi)
            else:
                self.isRunning = False
                
                

        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()

class VideoCamera(object):
    def __init__(self):
        # Open a camera
        self.cap = cv2.VideoCapture(0)
      
        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recordingThread = None
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        ret, frame = self.cap.read()
        flipped = cv2.flip(frame,0) #垂直翻轉
        #gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
        #ROI= gray[0:int(300), 0:int(500)] #寬500,高300

        if ret:
            #ret, jpeg = cv2.imencode('.jpg', ROI)
            ret, jpeg = cv2.imencode('.jpg', flipped)
            return jpeg.tobytes()
      
        else:
            return None

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()
