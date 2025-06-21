import os
import sys
from pathlib import Path

class ExtensionMedia:
    
    extension_videos = [".mp4", ".mkv", ".avi", ".mov", ".wmv"]
    extension_images = [".jpg", ".png", ".jpeg"]

    @staticmethod
    def get_path():
        if getattr(sys, 'frozen', False):
            ruta_script = Path(sys.executable).resolve()
        else:
            ruta_script = Path(__file__).resolve()
        return ruta_script.parent
    
    @classmethod
    def list_file_videos(cls):
        directorio_script = cls.get_path()
        files = os.listdir(directorio_script)
        videos = [
            file for file in files 
            if os.path.splitext(file)[1].lower() in cls.extension_videos
        ]
        return videos
    
    @classmethod
    def list_file_imagen(cls):
        directorio_script = cls.get_path()
        files = os.listdir(directorio_script)
        images = [
            file for file in files 
            if os.path.splitext(file)[1].lower() in cls.extension_images
        ]
        return images
    
