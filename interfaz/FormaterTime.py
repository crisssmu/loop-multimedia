from tkinter import *


def validate_hr(new_value):
    return (new_value == '' or (new_value.isdigit() and 0 <=int(new_value) <= 8))

def validate_min(new_value):
    return (new_value == '' or (new_value.isdigit() and 0 <= int(new_value) <= 60))

def validate_sg(new_value):
    return (new_value == '' or (new_value.isdigit() and 0 <= int(new_value) <= 59))

def command_hr(root):
    return (root.register(validate_hr), '%P')

def command_min(root):
    return (root.register(validate_min), '%P')    

def command_sg(root):
    return (root.register(validate_sg), '%P')

def format_time_label(root, string_time):
    time_label = Label(root, text=string_time, bg="#FDF8E1", fg="black", font=("Arial", 16), justify=LEFT)
    return time_label

def format_hour(root):
    time_hr = Entry(root, bg="#FFFFFF", fg="black", font=("Arial", 16), width=2, validate="key", validatecommand=command_hr(root))
    return time_hr

def format_minute(root):
    time_min = Entry(root, bg="#FFFFFF", fg="black", font=("Arial", 16), width=2, validate="key", validatecommand=command_min(root))
    return time_min

def format_second(root):
    time_seg = Entry(root, bg="#FFFFFF", fg="black", font=("Arial", 16), width=2, validate="key", validatecommand=command_sg(root))
    return time_seg

def separate(root):
    separate = Label(root, text=":", bg="#FDF8E1", fg="black", font=("Arial", 16))
    return separate

def focus_time(event):
    if event.widget.get() == "00":
        event.widget.delete(0, END)

def lost_focus_time(event):
    if event.widget.get() == "":
        event.widget.insert(0, "00")

