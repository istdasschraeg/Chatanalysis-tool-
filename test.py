from tkinter.simpledialog import *
from tkinter.filedialog import *
from tkinter import *
from tkinter import messagebox
top = Tk()

file_list=[]

top.geometry("1000x1000")
def show():
   filename = askopenfile()
   file_list.append


   
B1 = Button(top, text ="Input File Names", command = show)
B1.place(x=500,y=500)

top.mainloop()

