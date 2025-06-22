import os
import sys
from pathlib import Path
import inspect as ins

class ExtensionMedia:
    
    extension_videos = [".mp4", ".mkv", ".avi", ".mov", ".wmv"]
    extension_images = [".jpg", ".png", ".jpeg"]

    @staticmethod
    def get_path():
        if getattr(sys, 'frozen', False):
            return Path(sys.executable).parent
        else:
            frame = ins.stack()[1]
            rute = Path(frame.filename).resolve().parent
            return rute
    @classmethod
    def list_file_videos(cls, rute):
        if not rute.exists() or not rute.is_dir():
            raise ValueError("La ruta proporcionada no es un directorio o no existe.")
        videos = [
            file.name
            for file in rute.iterdir()
            if file.is_file() and file.suffix.lower() in cls.extension_videos
        ]
        return videos
    
    @classmethod
    def list_file_imagen(cls, rute):
        if not rute.exists() or not rute.is_dir():
            raise ValueError("La ruta proporcionada no es un directorio o no existe.")
        videos = [
            file.name
            for file in rute.iterdir()
            if file.is_file() and file.suffix.lower() in cls.extension_images
        ]
        return videos

    
