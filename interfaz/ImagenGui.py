from tkinter import *

def validate_hr (new_value):
    return (new_value == '' or (new_value.isdigit() and 0 <=int(new_value) <= 24))

def validate_min (new_value):
    return (new_value == '' or (new_value.isdigit() and 0 <= int(new_value) <= 60))

def validate_sg (new_value):
    return (new_value == '' or (new_value.isdigit() and 0 <= int(new_value) <= 59))

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


root = Tk()
root.title("Editar imagen")
window_width = 650  
window_height = 450
root.geometry(f"{window_width}x{window_height}")

center_x = int(window_width // 2)
center_y = int(window_height // 2)

playback_time_imagen = IntVar()

playback_time_label_imagen = Label(root, text="Tiempo de reproducción", bg="#FDF8E1", fg="black", font=("Arial", 16))
playback_time_label_imagen.place(x=center_x-250, y=center_y-30)

separator_time = Label(root, text=":", bg="#FDF8E1", fg="black", font=("Arial", 16))
separator_time.place(x=center_x+32, y=center_y-30)
separator_time2 = Label(root, text=":", bg="#FDF8E1", fg="black", font=("Arial", 16))
separator_time2.place(x=center_x+82, y=center_y-30)


command_hour = (root.register(validate_hr), '%P')
command_min = (root.register(validate_min), '%P')
command_second = (root.register(validate_sg), '%P')

time_hour = Entry(root, validate="key", validatecommand=command_hour)
time_hour.insert(0, '00')
time_hour.grid(row=0, column=1)
time_hour.config(bg="#FFFFFF", fg="black", font=("Arial", 16), width=2)
time_hour.place(x=center_x-0, y=center_y-30)
time_hour.bind("<FocusIn>", focus_hour)
time_hour.bind("<FocusOut>", lost_focus_hour)

time_min = Entry(root, validate="key", validatecommand=command_min)
time_min.insert(0, '00')
time_min.grid(row=0, column=1)
time_min.config(bg="#FFFFFF", fg="black", font=("Arial", 16), width=2)
time_min.place(x=center_x+50, y=center_y-30)

time_min.bind("<FocusIn>", focus_min)
time_min.bind("<FocusOut>", lost_focus_min)

time_seg = Entry(root, validate="key", validatecommand=command_second)
time_seg.insert(0, '00')
time_seg.grid(row=0, column=1)
time_seg.config(bg="#FFFFFF", fg="black", font=("Arial", 16), width=2)
time_seg.place(x=center_x+100, y=center_y-30)

time_seg.bind("<FocusIn>", focus_sg)
time_seg.bind("<FocusOut>", lost_focus_sg)

root.mainloop()