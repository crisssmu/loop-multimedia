import tkinter as tk 
from tkinter import *
from pathlib import Path
import video2 as vi
import monitor_utils as moni
import threading as th
import os

video_thread = None
ruta_script = Path(__file__).resolve()
directorio_script = ruta_script.parent

print(f"Ruta del script: {ruta_script}")
print(f"Directorio del script: {directorio_script}")

extension_videos = [".mp4", ".mkv", ".avi", ".mov", ".wmv"]
extension_images = [".jpg", ".png", ".jpeg"]

def list_file_imagen(directorio_script):
    files = os.listdir(directorio_script)
    images = [
        file for file in files 
        if os.path.splitext(file)[1].lower() in extension_images
    ]
    return images

def list_file_videos(directorio_script):
    files = os.listdir(directorio_script)
    videos = [
        file for file in files 
        if os.path.splitext(file)[1].lower() in extension_videos
    ]
    return videos

def out_entry(event):
    root.focus_set()
def focus_hour(event):
    if time_hour.get() == "00":
        time_hour.delete(0, END)

def lost_focus_hour(event):
    if time_hour.get() == "":
        time_hour.insert(0, "00")

def focus_min(event):
    if time_min.get() == "00":
        time_min.delete(0, END)

def lost_focus_min(event):
    if time_min.get() == "":
        time_min.insert(0, "00")

def focus_sg(event):
    if time_seg.get() == "00":
        time_seg.delete(0, END)

def lost_focus_sg(event):
    if time_seg.get() == "":
        time_seg.insert(0, "00")

def validate_hr (new_value):
    return (new_value == '' or (new_value.isdigit() and 0 <=int(new_value) <= 24))

def validate_min (new_value):
    return (new_value == '' or (new_value.isdigit() and 0 <= int(new_value) <= 60))

def validate_sg (new_value):
    return (new_value == '' or (new_value.isdigit() and 0 <= int(new_value) <= 59))

def select_file():
    if(select_media.get() == 0):
        for i, file in enumerate(list_file_videos(directorio_script)):
            if(select_archive.get() == i):
                menu_button_archive.config(text=file)
                print(f"Seleccionaste: {file}")
                return file
    else:
        for i, file in enumerate(list_file_imagen(directorio_script)):
            if(select_archive.get() == i):
                menu_button_archive.config(text=file)
                print(f"Seleccionaste: {file}")
                return file

def convert_seconds():
    total_seconds = int(time_hour.get()) * 3600 + int(time_min.get()) * 60 + int(time_seg.get())
    print(f"Total seconds: {total_seconds}")
    return total_seconds

def select_monitor():
    for i, monitor in enumerate(moni.get_moni()):
        if(select_moni.get() == i):
            menu_button_moni.config(text=monitor.name)
            print(f"Seleccionaste: {monitor.name} indice: {i}")
            return i

def play_media():
    vi.stop_event.clear()
    video_path = select_file()
    tiempo_intermedio = convert_seconds()
    index_moni = select_monitor()
    vi.loop_video(video_path, tiempo_intermedio, index_moni)

def block_entry():
    menu_button_moni.config(state=DISABLED)
    menu_button_archive.config(state=DISABLED)
    time_hour.config(state=DISABLED)
    time_min.config(state=DISABLED)
    time_seg.config(state=DISABLED)
    menu_button_media.config(state=DISABLED)

def button_play(event=None):
    global video_thread
    if video_thread and video_thread.is_alive():
        print("Video is already playing")
        return
    out_entry(event)
    thread = th.Thread(target=play_media)
    thread.daemon = False
    thread.start()
    
def on_closing():
    vi.stop_event.set()
    if video_thread and video_thread.is_alive():
        video_thread.join()
    root.destroy()

def see_widgets():
    time_label3.place(x=center_x-100, y=y_time_img)
    time_label4.place(x=center_x-50, y=y_time_img)

    time_hr_im.insert(0, '00')
    time_hr_im.grid(row=0, column=1)
    time_hr_im.config(bg="#FFFFFF", fg="black", font=("Arial", 16), width=2)
    time_hr_im.place(x=center_x-130, y=y_time_img)

    time_min_im.insert(0, '00')
    time_min_im.grid(row=0, column=1)
    time_min_im.config(bg="#FFFFFF", fg="black", font=("Arial", 16), width=2)
    time_min_im.place(x=center_x-80, y=y_time_img)

    time_seg_im.insert(0, '00')
    time_seg_im.grid(row=0, column=1)
    time_seg_im.config(bg="#FFFFFF", fg="black",font=("Arial", 16), width=2)
    time_seg_im.place(x=center_x-30, y=y_time_img)
def is_img_not_video():
    if(select_media.get() == 1):
        see_widgets()
    else:
        time_label3.place_forget()
        time_label4.place_forget()
        time_hr_im.place_forget()
        time_min_im.place_forget()
        time_seg_im.place_forget()
        y_moni = center_y+10

    return y_moni

def choose_type():
    type = select_media.get()
    menu_archive.delete(0, 'end')

    if(select_media.get() == 0):
        menu_button_media.config(text="Video")
        file = list_file_videos(directorio_script)
        
    else:
        menu_button_media.config(text="Imagen")
        file = list_file_imagen(directorio_script)

    for i, file in enumerate(file):
        menu_archive.add_radiobutton(label=file, value=i, variable=select_archive, command=select_file)

    return file
    
# Raiz de la interfaz
root = Tk()
# Tamaño de la ventana
window_width = 650  
window_height = 450

# Configuración de la ventana
root.title("Interfaz Grafica")
root.iconbitmap("icono.ico")
root.resizable(False, False)
root.attributes('-topmost',1)
root.config(bg = "#FDF8E1")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(window_width // 2)
center_y = int(window_height // 2)

root.geometry(f"{window_width}x{window_height}")

# Cuerpo de la interfaz

# Menu de configuracion
menu_bar = Menu(root)
root.config(menu=menu_bar, width=window_width, height=window_height)

menu_imagen = Menu(menu_bar)
menu_imagen.add_command(label="Editar")

menu_bar.add_cascade(label="Imagen", menu=menu_imagen)

# Tipo de archivo multimedia
select_media = IntVar(value=0)

menu_media_label = Label(root, text='Tipo:', bg="#FDF8E1", fg="black", font=("Arial", 16)).place(x=center_x+100, y=center_y-150)

menu_button_media = Menubutton(root,bg="#FFFFFF", fg="black", font=("Arial", 16))
menu_button_media.place(x=center_x+150, y=center_y-150)
menu_media = tk.Menu(menu_button_media, tearoff=False)
menu_button_media["menu"] = menu_media
menu_button_media.bind("<Return>", is_img_not_video)

menu_media.add_radiobutton(label="Video", value=0, variable=select_media, command=choose_type)
menu_media.add_radiobutton(label="Imagen", value=1, variable=select_media, command=choose_type)


# Menu despegable de archivos
archive_label = Label(root, text='Archivo:', bg="#FDF8E1", fg="black", font=("Arial", 16)).place(x=center_x-250, y=center_y-150)

select_archive = IntVar()

menu_button_archive = Menubutton(root, text='Selecciona el archivo' ,bg="#FFFFFF", fg="black", font=("Arial", 16))
menu_button_archive.place(x=center_x-130, y=center_y-150)
menu_archive = tk.Menu(menu_button_archive, tearoff=False)
menu_button_archive["menu"] = menu_archive

choose_type() #Eliges el tipo de archivo y se agregar la lista despegabl

# Variables tiempo
command_hour = (root.register(validate_hr), '%P')
command_min = (root.register(validate_min), '%P')
command_second = (root.register(validate_sg), '%P')

#hora
time_label = Label(root, text='Tiempo ' +'\nintermedio: ', bg="#FDF8E1", fg="black", font=("Arial", 16), justify=LEFT).place(x=center_x-250, y=center_y-80)

time_hour = Entry(root, validate="key", validatecommand=command_hour)
time_hour.insert(0, '00')
time_hour.grid(row=0, column=1)
time_hour.config(bg="#FFFFFF", fg="black", font=("Arial", 16), width=2)
time_hour.place(x=center_x-130, y=center_y-65)
time_hour.bind("<Return>", out_entry)

time_hour.bind("<FocusIn>", focus_hour)
time_hour.bind("<FocusOut>", lost_focus_hour)

tiempo1 = Label(root, text=':', bg="#FDF8E1", fg="black", font=("Arial", 16),width=1).place(x=center_x-100, y=center_y-65)

#Minutos
time_min = Entry(root, validate="key", validatecommand=command_min)
time_min.insert(0, '00')
time_min.grid(row=0, column=1)
time_min.config(bg="#FFFFFF", fg="black", font=("Arial", 16), width=2)
time_min.place(x=center_x-80, y=center_y-65)

time_min.bind("<FocusIn>", focus_min)
time_min.bind("<FocusOut>", lost_focus_min)
time_min.bind("<Return>", out_entry)

time_label2 = Label(root, text=':', bg="#FDF8E1", fg="black", font=("Arial", 16),width=1).place(x=center_x-50, y=center_y-65)

#Segundos
time_seg = Entry(root,textvariable='seg', validate="key", validatecommand=command_second)
time_seg.insert(0, '00')
time_seg.grid(row=0, column=1)
time_seg.config(bg="#FFFFFF", fg="black",font=("Arial", 16), width=2)
time_seg.place(x=center_x-30, y=center_y-65)

time_seg.bind("<FocusIn>", focus_sg)
time_seg.bind("<FocusOut>", lost_focus_sg)
time_seg.bind("<Return>", out_entry)

y_time_img = center_y-10
# Tiempo de duracion para mostrar una imagen

time_img_label = Label(root, text='Tiempo ' +'\nimagen: ', bg="#FDF8E1", fg="black", font=("Arial", 16), justify=LEFT)



time_hr_im = Entry(root, validate="key", validatecommand=command_hour)

time_hr_im.bind("<FocusIn>", focus_hour)
time_hr_im.bind("<FocusOut>", lost_focus_hour)
time_hr_im.bind("<Return>", out_entry)

time_label3 = Label(root, text=':', bg="#FDF8E1", fg="black", font=("Arial", 16),width=1)


time_min_im = Entry(root, validate="key", validatecommand=command_min)


time_min_im.bind("<FocusIn>", focus_min)
time_min_im.bind("<FocusOut>", lost_focus_min)
time_min_im.bind("<Return>", out_entry)

time_label4 = Label(root, text=':', bg="#FDF8E1", fg="black", font=("Arial", 16),width=1)


time_seg_im = Entry(root, validate="key", validatecommand=command_second)


time_seg_im.bind("<FocusIn>", focus_sg)
time_seg_im.bind("<FocusOut>", lost_focus_sg)
time_seg_im.bind("<Return>", out_entry)

y_moni = center_y-10

choose_moni = Label(root, text='Monitor', bg="#FDF8E1", fg="black", font=("Arial", 16)).place(x=center_x-250, y=y_moni)

# Menu desplegable
select_moni = tk.IntVar()

menu_button_moni = Menubutton(root, text='Selecciona el monitor' ,bg="#FFFFFF", fg="black", font=("Arial", 16))
menu_moni  = tk.Menu(menu_button_moni , tearoff=False)
menu_button_moni ["menu"] = menu_moni

for i, monitor in enumerate(moni.get_moni()) :
    menu_moni.add_radiobutton(label=monitor.name, value=i, variable = select_moni, command=select_monitor)

menu_button_moni.grid(row=len(moni.get_moni()), column=1)
menu_button_moni.place(x=center_x-130, y=y_moni)

# Boton para reproducir
button = Button(root, text='Reproducir', command=block_entry)
button.place(x=center_x+50, y=center_y+100)
button.bind("<Button-1>", button_play)

button_exit = Button(root, text='Salir', command=on_closing)
button_exit.place(x=center_x-50, y=center_y+100)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

#prueba