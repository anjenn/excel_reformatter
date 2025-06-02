import tkinter as tk
from tkinter import font

######################################################################
# 프로그램 인터페이스
######################################################################
root = tk.Tk()

def show_frame(frame):
    frame.tkraise()

container = tk.Frame(root)
container.pack(fill='both', expand=True)
container.pack_propagate(False)  # Don't shrink to fit contents

# Center this frame in the window
container.place(relx=0.5, rely=0.5, anchor='center')  # Center frame

# --- Define pages (as frames)
main_page = tk.Frame(container)
st_sales_page = tk.Frame(container)
lt_sales_page = tk.Frame(container)


for frame in (main_page, st_sales_page, lt_sales_page):
    frame.grid(row=0, column=0, sticky='nsew')