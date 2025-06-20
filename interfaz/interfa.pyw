import tkinter as tk 
from tkinter import *
from pathlib import Path

def call_back():
    print('Boton pulsado')

raiz = Tk()

window_width = 650  
window_height = 450

raiz.title("Interfaz Grafica")
raiz.iconbitmap("icono.ico")
raiz.resizable(False, False)
raiz.attributes('-topmost',1)
raiz.config(bg = "#FDF8E1")

screen_width = raiz.winfo_screenwidth()
screen_height = raiz.winfo_screenheight()

center_x = int(window_width // 2)
center_y = int(window_height // 2)

raiz.geometry(f"{window_width}x{window_height}")
archive = Label(raiz, text='Inserta tu archivo', bg="#FDF8E1", fg="black", font=("Arial", 16)).place(x=center_x-250, y=center_y-100)
menu_button = Menubutton(raiz, text='Selecciona el archivo', bg="#FFFFFF", fg="black", font=("Arial", 16))
menu_button.place(x=center_x-50, y=center_y-100)
ruta = Path("C:/Users/Cristina/Documents/Codigo/video/interfaz")

videos = list(ruta.glob("*.mp4"))

archivos = []

for video in videos:
    archivos.append(video.name)


menu = tk.Menu(menu_button, tearoff=False)

for archivo in archivos:    
    menu.add_radiobutton(label=archivo)

menu_button["menu"] = menu
menu_button.grid(row=len(archivos), column=1)
menu_button.place(x=center_x-50, y=center_y-100)

tiempo1 = Label(raiz, text='Tiempo espera: ', bg="#FDF8E1", fg="black", font=("Arial", 16)).place(x=center_x-250, y=center_y-30)
text_time = Entry(raiz)
text_time.grid(row=0, column=1)
text_time.config(bg="#FFFFFF", fg="black", font=("Arial", 16))
text_time.place(x=center_x-50, y=center_y-30)


button = Button(raiz, text='Reproducir', command=call_back)
button.place(x=center_x-50, y=center_y+50)

raiz.mainloop()

