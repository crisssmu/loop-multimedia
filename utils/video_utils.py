import cv2
import datetime
from utils.monitor_utils import Monitor
import pygame
import threading as th

class Video:

    def __init__(self, name, stop_event=None):
        self.name = name
        self.stop_event = stop_event or th.Event()
        
    def __str__(self):
        return f"Video: {self.name}"
    
    def get_video(self):
        cap = cv2.VideoCapture(self.name)
        return cap
   
    def get_fps(self):
        cap = self.get_video()
        return  cap.get(cv2.CAP_PROP_FPS)
        
   
    def get_frames(self):
        cap = self.get_video()
        return int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
    
    def get_duration(self):
        fps = self.get_fps()
        frames = self.get_frames()
        duration = ''
        if fps > 0:
            duration_sec = frames / fps
        else:
            duration_sec = 0

        duration = str(datetime.timedelta(seconds=int(duration_sec))) 

        return duration
    
    def stop(self):
        self.stop_event.set()
    
    def watch_video(self, index_moni):
        try:
            Monitor.get_monitores()
            moni, windowms = Monitor.choose_monitor(index_moni)
            
            cap = self.get_video()

            if not cap.isOpened():
                print("Error opening video stream or file")
                exit()
            
            fps = self.get_fps()
            total_frames = self.get_frames()
            duration = self.get_duration()
            cont_frames = 0

            print('Duracion del video: ', duration)
            def escalar_frame(frame):
                return cv2.resize(frame, (moni.width, moni.height))
            
            reloj = pygame.time.Clock()
            
            while not self.stop_event.is_set() and cont_frames < total_frames:
                ret, frame = cap.read()
                if not ret:
                    break

                cont_frames += 1

                frame = escalar_frame(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

                windowms.blit(frame, (0, 0))
                pygame.display.update()
                reloj.tick(fps)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.stop_event.set()

            print('Reproduccion finalizada')
            cap.release()
            pygame.quit()
        except KeyboardInterrupt:
            print('Programa finalizado por el usuario')
            self.stop_event.set()

        





    