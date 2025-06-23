
import interfaz.gui as gui
from utils.extension_media import ExtensionMedia as ext
from utils.monitor_utils import Monitor as monitor 

path = ext.get_path()
imagenes = ext.list_file_imagen(path)
videos = ext.list_file_videos(path)
monitors = monitor.get_monitores()
list_monitor = monitor.list_monitors()

print(path)
print(imagenes)
print(videos)

gui.start_interface(videos, imagenes, monitors)
