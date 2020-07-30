from tkinter import *
import time
import os
from PIL import Image
root = Tk()
root.title("Download Complete")
frames = [PhotoImage(file='/root/Downloads/20200729_210949.gif',format = 'gif -index %i' %(i)) for i in range(87)]

def update(ind):

    try:
        frame = frames[ind]
        ind += 1
        label.config(image=frame)
        root.after(20, update, ind)
    except:
        root.destroy()
        pass
        # ind=0
        # frame = frames[ind]
        # label.configure(image=frame)
        # root.after(40, update, ind)
label = Label(root)
label.pack()
    
root.after(0, update, 0)
root.mainloop()
