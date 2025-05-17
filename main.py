import tkinter as tk

def say_hello():
    label.config(text="안녕하세요!")

root = tk.Tk()
root.title("나의 첫 윈도우 프로그램")

label = tk.Label(root, text="버튼을 눌러보세요.")
label.pack()

button = tk.Button(root, text="눌러주세요", command=say_hello)
button.pack()

root.mainloop()
