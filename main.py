import customtkinter
import tkinter
import pymem
import gc
import requests
from plyer import notification

# Constants
APP_WIDTH = 350
APP_HEIGHT = 300
ENTRY_WIDTH = 120
ENTRY_HEIGHT = 27
BORDER_WIDTH = 0
CORNER_RADIUS = 0

# Create the application
app = customtkinter.CTk()
app.configure(bg='red')
app.geometry(f'{APP_WIDTH}x{APP_HEIGHT}')
app.title('AG7 String Deleter')

# Create labels and entries
label = customtkinter.CTkLabel(app, text='Made by AG7', text_color='pink')
label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

proc_name_entry = customtkinter.CTkEntry(app, placeholder_text='Process name', width=ENTRY_WIDTH, height=ENTRY_HEIGHT, border_width=BORDER_WIDTH, corner_radius=CORNER_RADIUS)
proc_name_entry.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

address_entry = customtkinter.CTkEntry(app, placeholder_text='Address', width=ENTRY_WIDTH, height=ENTRY_HEIGHT, border_width=BORDER_WIDTH, corner_radius=CORNER_RADIUS)
address_entry.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

length_entry = customtkinter.CTkEntry(app, placeholder_text='Length', width=ENTRY_WIDTH, height=ENTRY_HEIGHT, border_width=BORDER_WIDTH, corner_radius=CORNER_RADIUS)
length_entry.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

def delete_string():
    proc_name = proc_name_entry.get()
    address = int(address_entry.get(), 0)
    length = int(length_entry.get(), 0)

    try:
        pm = pymem.Pymem(proc_name)
        pm.read_bytes(address, length)
        rs = pm.read_string(address, length)
        notification.notify(title='String Check', message='Refresh your Process Hacker and take a look if the string is deleted', app_icon=None, timeout=10)
        print(rs)
        value = '.' * length
        pm.write_string(address, value)
        gc.collect()
        notification.notify(title='String Check', message='Refresh your Process Hacker and take a look if the string is deleted', app_icon=None, timeout=10)
    except Exception as e:
        print(f'Error: {e}')

button = customtkinter.CTkButton(app, text='Remove string', command=delete_string, width=ENTRY_WIDTH, height=ENTRY_HEIGHT + 5, border_width=BORDER_WIDTH, corner_radius=CORNER_RADIUS, fg_color='purple', hover_color='#67546C')
button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

app.mainloop()