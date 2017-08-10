from tkinter import *
# import simple as si
root = Tk()

def frame():
    # line('890t345gergredfgdf')
    # line('890t345gergredfgddfsff')
    root.mainloop()

def line(text):
    Label(root, text=text).pack()

def button(text, func):
    Button(root, text=text, command=func).pack()
