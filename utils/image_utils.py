import cv2
import time
import pygame
from utils.monitor_utils import Monitor
import threading as th
import win32gui, win32con



class Image:
    def __init__(self, name, stop_event=None):
        self.name = name
        self.stop_event = stop_event or th.Event()

    def __str__(self):
        return f"Image: {self.name}"
        
    def get_image(self):
        img = cv2.imread(self.name, cv2.IMREAD_COLOR)
        return img
    
    def stop(self):
        self.stop_event.set()

    def watch_image(self, index_moni, duration_seconds):
        try:
            Monitor.get_monitores()
            moni = Monitor.select_monitor(index_moni)
            windowms = Monitor.send_media_to_monitor(moni)
            
            img = self.get_image()

            if img is None:
                print("Error opening video stream or file")
                exit()

            img =  cv2.resize(img, (moni.width, moni.height))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_s = pygame.surfarray.make_surface(img.swapaxes(0, 1))

            clock = pygame.time.Clock()
            start_time = time.time()

            hwnd = pygame.display.get_wm_info()["window"]
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, moni.x, moni.y, moni.width, moni.height, win32con.SWP_SHOWWINDOW)
        
            while not self.stop_event.is_set() and (time.time() - start_time) <= duration_seconds:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.stop_event.set()

                    windowms.blit(img_s, (0, 0))
                    pygame.display.update()
                    clock.tick(60)
            pygame.quit()
        except KeyboardInterrupt:
            print('Programa finalizado por el usuario')
            self.stop_event.set()
        
