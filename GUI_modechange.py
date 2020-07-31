#!/usr/bin/env python3
from PIL import Image
import os,sys,subprocess,shutil,json,time,random,requests,urllib.request,keyboard
import tkinter as tk
from functools import partial
import tkinter.messagebox as tkm
import datetime
import threading
#############################
# functions
def gotodir(name):
    global parent_folder
    if os.getcwd() != parent_folder:
        os.chdir(name)


def start_operating():
    global var,time_var,dic,parent_folder,start_op,top
    print(var.get(),time_var.get())
    if(var.get()==0 and time_var.get()==1 and dic["period"]!=None):
        top.destroy()
        while not keyboard.is_pressed('ctrl+space'):
            nam=dic["current_mode"].replace(" ","_")
            lst=os.listdir(parent_folder+"{}".format(nam))
            try:
                fl=open(parent_folder+nam+"/last.txt","r")
                lt=fl.read().strip() 
                lst.remove("last.txt")
                fl.close()
            except:
                lt=None
            wall=random.choice(lst)
            while wall==lt:
                wall=random.choice(lst)
            fl=open(parent_folder+nam+"/last.txt","w")
            fl.write(wall)
            fl.close()
            path=parent_folder+nam+"/"+wall
            set_wall(path)
            for i in range(int(dic["period"])*10):
                time.sleep(0.1)
                if(keyboard.is_pressed('ctrl+space')):
                    exit(1)

    elif(var.get()==1 and time_var.get()==1 and dic["period"]!=None):
        top.destroy()
        while not keyboard.is_pressed('ctrl+space'):
            nam=dic["current_mode"].replace(" ","_")
            lst=os.listdir(parent_folder+"{}".format(nam))
            try:
                lst.remove("last.txt")
            except:
                pass
            for wall in lst:
                path=parent_folder+nam+"/"+wall
                set_wall(path)
                for i in range(int(dic["period"])*10):
                    time.sleep(0.1)
                    if(keyboard.is_pressed('ctrl+space')):
                        exit(1)

    elif(var.get()==0 and time_var.get()==0 and dic["time"][0]!=None and dic["time"][1]!=None):
        top.destroy()
        while not keyboard.is_pressed('ctrl+space'):
            current_time=datetime.datetime.now()
            if(current_time.hour==int(dic["time"][0]) and current_time.minute==int(dic["time"][1])):
                nam=dic["current_mode"].replace(" ","_")
                lst=os.listdir(parent_folder+"{}".format(nam))
                try:
                    fl=open(parent_folder+nam+"/last.txt","r")
                    lt=fl.read().strip() 
                    lst.remove("last.txt")
                    fl.close()
                except:
                    lt=None
                wall=random.choice(lst)
                while wall==lt:
                    wall=random.choice(lst)
                fl=open(parent_folder+nam+"/last.txt","w")
                fl.write(wall)
                fl.close()
                path=parent_folder+nam+"/"+wall
                set_wall(path)
                for i in range(1200):
                    time.sleep(0.1)
                    if(keyboard.is_pressed('ctrl+space')):
                        exit(1)

    elif(var.get()==1 and time_var.get()==0 and dic["time"][0]!=None and dic["time"][1]!=None):
        top.destroy()
        nam=dic["current_mode"].replace(" ","_")
        lst=os.listdir(parent_folder+"{}".format(nam))
        lst.remove("last.txt")
        for wall in lst:
            current_time=datetime.datetime.now()
            while (current_time.hour!=int(dic["time"][0]) and current_time.minute!=int(dic["time"][1])):
                current_time=datetime.datetime.now()
                for i in range(600):
                    time.sleep(0.1)
                    if(keyboard.is_pressed('ctrl+space')):
                        exit(1)
            if not keyboard.is_pressed('ctrl+space'):
                break
            path=parent_folder+nam+"/"+wall
            set_wall(path)


def change_time():
    global win7,en7_1,en7_2,dic
    dic["time"]=en7_1.get(),en7_2.get()
    fst=open("/root/Python_codes/log.txt","w")
    fst.write(json.dumps(dic))
    fst.close()
    print("Time has been changed")
    win7.destroy()

def change_sch_gui():
    global win7,en7_1,en7_2,dic
    if "time" not in dic:
        dic["time"]=(None,None)
    win7=tk.Tk()
    win7.title("Change Time")
    canvas7= tk.Canvas(win7,height=400,width=400,bg="black",highlightbackground="black",highlightthickness=0)
    canvas7.pack()
    par_frame7=tk.Frame(canvas7,bd=0,bg="black",highlightbackground="black",highlightthickness=0)
    par_frame7.pack()
    la7_1=tk.Label(par_frame7, text="Hour",fg="white",bg="black",justify="left",highlightbackground="black",highlightthickness=0)
    la7_1.grid(column=0,row=0)
    en7_1=tk.Entry(par_frame7,fg="white",bg="black")
    en7_1.grid(column=1,row=0)
    if(dic["time"][0]!=None):
        en7_1.insert(0,dic["time"][0])
    la7_2=tk.Label(par_frame7, text="Minutes",fg="white",bg="black",justify="left",highlightbackground="black",highlightthickness=0)
    la7_2.grid(column=0,row=1)
    en7_2=tk.Entry(par_frame7,fg="white",bg="black")
    en7_2.grid(column=1,row=1)
    if(dic["time"][1]!=None):
        en7_2.insert(0,dic["time"][1])
    change_time_button=tk.Button(canvas7,text="Set",fg="white",bg="black",activeforeground="white",activebackground="#323232",command= change_time)#
    change_time_button.pack()



def change_period():
    global win3,en3,dic
    dic["period"]=en3.get()
    fst=open("/root/Python_codes/log.txt","w")
    fst.write(json.dumps(dic))
    fst.close()
    print("Period has been changed")
    win3.destroy()

def change_period_gui():
    global dic,win3,en3
    win3=tk.Tk()
    win3.title("Config Settings")
    canvas3= tk.Canvas(win3,height=400,width=400,bg="black",highlightbackground="black",highlightthickness=0)
    canvas3.pack()
    par_frame3=tk.Frame(canvas3,bd=0,bg="black",highlightbackground="black",highlightthickness=0)
    par_frame3.pack()
    la3=tk.Label(par_frame3, text="Period",fg="white",bg="black",justify="left",highlightbackground="black",highlightthickness=0)
    la3.grid(column=0,row=0)
    en3=tk.Entry(par_frame3,fg="white",bg="black")
    en3.grid(column=1,row=0)
    en3.insert(0,dic["period"])
    change_period_button=tk.Button(canvas3,text="Set",fg="white",bg="black",activeforeground="white",activebackground="#323232",command= change_period)#
    change_period_button.pack()

def changemode(i,dic):
    global labels
    for idx in range(len(labels)):
        if(labels[idx].cget("text")==dic["current_mode"]):
            labels[idx].config(fg="white")
            break
    dic["current_mode"]=dic["modes"][i]
    labels[i].config(fg="red")
    fst=open("/root/Python_codes/log.txt","w")
    fst.write(json.dumps(dic))
    fst.close()
    print(dic["modes"][i], "has been activated")

def addmode_gui():
    global dic,en2,win2
    win2=tk.Tk()
    win2.title("Config Settings")
    canvas2= tk.Canvas(win2,height=400,width=400,bg="black",highlightbackground="black",highlightthickness=0)
    canvas2.pack()
    par_frame2=tk.Frame(canvas2,bd=0,bg="black",highlightbackground="black",highlightthickness=0)
    par_frame2.pack()
    la2=tk.Label(par_frame2, text="Name",fg="white",bg="black",justify="left",highlightbackground="black",highlightthickness=0)
    la2.grid(column=0,row=0)
    en2=tk.Entry(par_frame2,fg="white",bg="black")
    en2.grid(column=1,row=0)
    add_button=tk.Button(canvas2,text="Add",fg="white",bg="black",activeforeground="white",activebackground="#323232",command= addmode)#
    add_button.pack()
    ############

def addmode():
    global en2,dic,labels,del_buttons,act_buttons,ph_buttons
    s=en2.get()
    try:
        ss=s.replace(" ","_")
        os.mkdir(dic["parent_folder"]+"{}".format(ss))
        dic["modes"].append(s)
        fst=open("/root/Python_codes/log.txt","w")
        fst.write(json.dumps(dic))
        fst.close()
        i=len(labels)
        labels.append(tk.Label(f2,text=dic["modes"][i],fg="white",bg="black",justify="left"))
        labels[i].grid(row=i,column=0)
        act_buttons.append(tk.Button(f2,text="Activate",fg="white",bg="black",activeforeground="white",activebackground="#323232",command=partial(changemode,i,dic)))
        act_buttons[i].grid(row=i,column=1)
        del_buttons.append(tk.Button(f2,text="Delete Mode",fg="white",bg="black",activeforeground="white",activebackground="#323232",command=partial(delmode,i,dic)))
        del_buttons[i].grid(row=i,column=2)
        ph_buttons.append(tk.Button(f2,text="Add Photos",fg="white",bg="black",activeforeground="white",activebackground="#323232",command=partial(addphotos_gui,i)))
        ph_buttons[i].grid(row=i,column=3)

        print(s, "has been added")
    except:
        print("Mode couldn't be added")
    win2.destroy()

def delmode(i,dic):
    global parent_folder,labels,del_buttons,act_buttons,ph_buttons
    s=dic["modes"][i]
    try:
        dic["modes"].remove(s)
        st=s.replace(" ","_")
        shutil.rmtree(parent_folder+"{}".format(st))
        fst=open("/root/Python_codes/log.txt","w")
        fst.write(json.dumps(dic))
        fst.close()
        labels[i].destroy()
        labels.pop(i)
        del_buttons[i].destroy()
        del_buttons.pop(i)
        ph_buttons[i].destroy()
        ph_buttons.pop(i)
        act_buttons[i].destroy()
        act_buttons.pop(i)
        for idx in range(i,len(labels)):
            del_buttons[i].config(row=i)
            act_buttons[i].config(row=i)
            ph_buttons[i].config(row=i)

        print("Mode deleted")
    except:
        print("Mode doesn't exist")


def addphotos_gui(i):
    global win4
    win4=tk.Tk()
    win4.title("Add Photos")
    canvas4= tk.Canvas(win4,height=400,width=400,bg="black",highlightbackground="black",highlightthickness=0)
    canvas4.pack()
    par_frame4=tk.Frame(canvas4,bd=0,bg="black",highlightbackground="black",highlightthickness=0)
    par_frame4.pack()
    folder_button=tk.Button(par_frame4,text="Select from folder",fg="white",bg="black",activeforeground="white",activebackground="#323232",command=partial(add_ph_fl,i))
    folder_button.pack(side="left")
    download_button=tk.Button(par_frame4,text="Download Images",fg="white",bg="black",activeforeground="white",activebackground="#323232",command=partial(add_ph_dw,i))
    download_button.pack(side="left")

def add_ph_dw(i):
    global win4,win5,e1,e2
    win4.destroy()
    win5= tk.Tk()
    win5.title("Image Downloader")

    canvas5= tk.Canvas(win5,height=400,width=400,bg="black",highlightbackground="black",highlightthickness=0)
    canvas5.pack()

    pframe=tk.Frame(canvas5,bd=0,highlightbackground="black",highlightthickness=0)
    pframe.pack()
    fr1=tk.Frame(pframe,bd=0,bg="black",highlightbackground="black",highlightthickness=0,pady=3)
    fr1.pack(side="left")
    fr2=tk.Frame(pframe,bd=0,bg="black",highlightbackground="black",highlightthickness=0)
    fr2.pack(side="right")

    L1=tk.Label(fr1, text="Search Text   ",fg="white",bg="black",justify="left",highlightbackground="black",highlightthickness=0)
    L1.pack()#
    e1=tk.Entry(fr2,fg="white",bg="black")
    e1.pack()#side="left"

    L2=tk.Label(fr1, text="Search Count ",fg="white",bg="black",justify="left",highlightbackground="black",highlightthickness=0)#
    L2.pack()#side="left"
    e2=tk.Entry(fr2,fg="white",bg="black")#
    e2.pack()#side="right"
    w2 = tk.Button(canvas5, text="Download",command= partial(gimg_download,i),fg="white",bg="black",activebackground="#323232")#
    w2.pack()


def add_ph_fl(i):
    global dic,en6,win6,win4
    win4.destroy()
    win6=tk.Tk()
    win6.title("Add photos from folder")
    canvas6= tk.Canvas(win6,height=400,width=400,bg="black",highlightbackground="black",highlightthickness=0)
    canvas6.pack()
    par_frame6=tk.Frame(canvas6,bd=0,bg="black",highlightbackground="black",highlightthickness=0)
    par_frame6.pack()
    la6=tk.Label(par_frame6, text="Name",fg="white",bg="black",justify="left",highlightbackground="black",highlightthickness=0)
    la6.grid(column=0,row=0)
    en6=tk.Entry(par_frame6,fg="white",bg="black")
    en6.grid(column=1,row=0)
    copy_button=tk.Button(canvas6,text="Add",fg="white",bg="black",activeforeground="white",activebackground="#323232",command= partial(addphotos,i,dic))#
    copy_button.pack()

def addphotos(i,dic):
    global en6,win6
    mode=dic["modes"][i]
    src=en6.get()
    lst=os.listdir(src)
    for fil in lst:
        if(src[-1]!='/'):
            src+="/"
        shutil.copy(src+fil,parent_folder+"/{}".format(mode))
    print("Pictures have been added")
    win6.destroy()


def set_wall(wallp):
    st='"{}"'.format(wallp)
    subprocess.call(['gsettings','set','org.gnome.desktop.background' ,'picture-uri',st])

def setconfig():
    global ke,cse,parent_folder,win,canvas1,dic
    win=tk.Tk()
    win.title("Config Settings")
    canvas1= tk.Canvas(win,height=400,width=400,bg="black",highlightbackground="black",highlightthickness=0)
    canvas1.pack()
    par_frame=tk.Frame(canvas1,bd=0,bg="black",highlightbackground="black",highlightthickness=0)
    par_frame.pack()
    f3=tk.Frame(par_frame,bd=0,bg="black",highlightbackground="black",highlightthickness=0)
    f3.pack(side="left")
    f4=tk.Frame(par_frame,bd=0,bg="black",highlightbackground="black",highlightthickness=0,pady=2)
    f4.pack(side="right")

    L3=tk.Label(f3, text="Key               ",fg="white",bg="black",justify="left",highlightbackground="black",highlightthickness=0)
    L3.pack()
    global e3
    e3=tk.Entry(f4,fg="white",bg="black")
    if ke!=None:
        e3.insert(0,ke)
    e3.pack()

    L4=tk.Label(f3, text="CSE ID           ",fg="white",bg="black",justify="left",highlightbackground="black",highlightthickness=0)
    L4.pack()

    global e4
    e4=tk.Entry(f4,fg="white",bg="black")
    if cse!=None:
        e4.insert(0,cse)
    e4.pack()
    L5=tk.Label(f3, text="Parent Folder",fg="white",bg="black",justify="left",highlightbackground="black",highlightthickness=0)
    L5.pack()
    global e5
    e5=tk.Entry(f4,fg="white",bg="black")
    if parent_folder!=None:
        e5.insert(0,parent_folder)
    e5.pack()
    w3 = tk.Button(canvas1,text="Save", command= saveconfig,fg="white",bg="black",activeforeground="white",activebackground="#323232",bd=0)
    w3.pack()

def saveconfig():
    global ke,cse,parent_folder,e3,e4,e5,win,dic
    fst=open("/root/Python_codes/log.txt","w")
    ke=e3.get()
    cse=e4.get()
    parent_folder=e5.get()
    if parent_folder[-1]!="/":
        parent_folder+="/"
    dic["g_key"],dic["G_cse"],dic["parent_folder"]=ke,cse,parent_folder
    fst.write(json.dumps(dic))
    fst.close()
    win.destroy()


def gimg_download(i):
    global ke,cse,parent_folder,e1,e2,dic,win5
    if cse==None or ke==None or parent_folder==None:
        print("error")
        return

    site="https://www.googleapis.com/customsearch/v1?"
    name=e1.get()+" pc wallpaper"
    num=e2.get()
    # print(name,num,ke,cse,parent_folder)
    page=requests.get(site,params={"key":ke,"cx":cse,"q":name,"num":num,"start":"0","searchType":"image","imgSize":"huge"})
    diction=page.json()
    lst=[]
    if "items" not in diction:
        print("No results found!")
    else:
        ls=name.split()
        new_name="_".join(ls)
        gotodir(parent_folder+"/"+dic["modes"][i])
        for di in diction["items"]:
            sty=di["fileFormat"]
            sr=sty[6:len(sty)]
            lst.append((di["link"],sr))
        i=0
        for link in lst:
            try:
                urllib.request.urlretrieve(link[0],new_name+"_"+str(i)+'.'+link[1])
                print("Downloaded "+ str(i+1)+" image(s)")
                i+=1
            except:
                print("There was some error")
    subprocess.call(["python3","/root/Python_codes/wallpaper_change/animat.py"])
    win5.destroy()
############################################################################
# Dictionary
try:
    file_obj=open("/root/Python_codes/log.txt","r")
    st=file_obj.read()
    dic=json.loads(st)
    # cse,ke,parent_folder=dic[]
except:
    dic={"modes":[],"current_mode":None,"period":10,"g_key":None,"G_cse":None,"parent_folder":None,"time":(None,None)}
if dic["parent_folder"]!=None and dic["parent_folder"][-1]!="/":
    dic["parent_folder"]+="/"
ke,cse,parent_folder=dic["g_key"],dic["G_cse"],dic["parent_folder"]

print(dic)
##########################################################################
##GIF
# im = Image.open("/root/Downloads/200.gif")
# count=0
# try:
    # while True:
        # im.seek(im.tell()+1)
        # count+=1
# except EOFError:
    # pass

# global anim,anim_label,ani_frames
# anim = tk.Tk()
# ani_frames = [tk.PhotoImage(file='/root/Downloads/200.gif',format = 'gif -index %i' %(i)) for i in range(count)]
# anim_label = tk.Label(anim)
# anim_label.pack()
# anim.after(0,update,0)

#########################################################################
############################################################################
############################################################################
############################################################################

# GUI

top=tk.Tk()
top.title("ModeChanger")
top.geometry()
############################################################################
# Canvas
canvas=tk.Canvas(top,height=1080,width=1920,bg="black",bd=1)
canvas.pack()
############################################################################
# top buttons
top_Frame=tk.Frame(canvas,bd=0,bg="black")
top_Frame.pack()
add_mode=tk.Button(top_Frame,text="Add Mode",fg="white",bg="black",activeforeground="white",activebackground="#323232",command=addmode_gui)
add_mode.pack(side="left")
chg_period=tk.Button(top_Frame,text="Change Period",fg="white",bg="black",activeforeground="white",activebackground="#323232",command=change_period_gui)
chg_period.pack(side="left")
chg_sch=tk.Button(top_Frame,text="Change Switching Time",fg="white",bg="black",activeforeground="white",activebackground="#323232",command=change_sch_gui)
chg_sch.pack(side="left")
############################################################################
# sub menu
menuBar=tk.Menu(top,bg="black",fg="white")
top.config(menu=menuBar)
subMenu=tk.Menu(menuBar, tearoff=0,fg="white",bg="black")
menuBar.add_cascade(label="Settings",menu=subMenu,activeforeground="white",activebackground="#323232")
subMenu.add_command(label="Config Settings",command=setconfig,activeforeground="white",activebackground="#323232")
############################################################################
# MODES
f1=tk.Frame(canvas,bd=0,bg="black")
f1.pack()
l1=tk.Label(f1,text="Available Modes",fg="white",bg="black",pady=9)
l1.pack()
global f2
f2=tk.Frame(f1,bd=0,bg="black",pady=7,padx=7)
f2.pack()
labels=[None for i in range(len(dic["modes"]))]
act_buttons=labels[:]
del_buttons=labels[:]
ph_buttons=labels[:]
for i in range(len(dic["modes"])):
    labels[i]=tk.Label(f2,text=dic["modes"][i],fg="white",bg="black",justify="left")
    labels[i].grid(row=i,column=0)
    if dic["modes"][i]==dic["current_mode"]:
        labels[i].config(fg="red")
    act_buttons[i]=tk.Button(f2,text="Activate",fg="white",bg="black",activeforeground="white",activebackground="#323232",command=partial(changemode,i,dic))
    act_buttons[i].grid(row=i,column=1)
    del_buttons[i]=tk.Button(f2,text="Delete Mode",fg="white",bg="black",activeforeground="white",activebackground="#323232",command=partial(delmode,i,dic))
    del_buttons[i].grid(row=i,column=2)
    ph_buttons[i]=tk.Button(f2,text="Add Photos",fg="white",bg="black",activeforeground="white",activebackground="#323232",command=partial(addphotos_gui,i))
    ph_buttons[i].grid(row=i,column=3)
############################################################################
# Selecting Procedure
selection_frame=tk.Frame(canvas,bd=0,bg="black",highlightbackground="black",pady=7)
selection_frame.pack()
prolabel=tk.Label(selection_frame,text="Selection Method",fg="white",bg="black",justify="left")
prolabel.pack()
global var
var=tk.IntVar()
pro1=tk.Radiobutton(selection_frame,text="Random Selection",highlightbackground="black",fg="white",selectcolor="black",bg="black",variable=var,value=0,activeforeground="white",activebackground="#323232",borderwidth=0)
pro1.pack(side="left")
pro2=tk.Radiobutton(selection_frame,text="Cycle Through",variable=var,fg="white",highlightbackground="black",selectcolor="black",bg="black",value=1,activeforeground="white",activebackground="#323232",borderwidth=0)
pro2.pack(side="left")
###########################################################################
# time dependency
time_frame=tk.Frame(canvas,bd=0,bg="black",highlightbackground="black",pady=7)
time_frame.pack()
time_label=tk.Label(time_frame,text="Oscillation Criteria",fg="white",bg="black",justify="left")
time_label.pack()
global time_var
time_var=tk.IntVar()
time_1=tk.Radiobutton(time_frame,text="Scheduled",highlightbackground="black",fg="white",selectcolor="black",bg="black",variable=time_var,value=0,activeforeground="white",activebackground="#323232",borderwidth=0)
time_1.pack(side="left")
time_2=tk.Radiobutton(time_frame,text="Periodic",variable=time_var,fg="white",highlightbackground="black",selectcolor="black",bg="black",value=1,activeforeground="white",activebackground="#323232",borderwidth=0)
time_2.pack(side="left")
###########################################################################
start_op=tk.Button(canvas,pady=7,text="start",fg="white",bg="black",activeforeground="white",activebackground="#323232",command=start_operating)
start_op.pack()
###########################################################################
top.mainloop()

############################################################################
############################################################################
############################################################################3

# if(dic["current_mode"]!=None):
    # while True:
        # nam=dic["current_mode"].replace(" ","_")
        # lst=os.listdir("/root/Pictures/Wallpapers/{}".format(nam))
        # try:
            # fl=open("/root/Pictures/Wallpapers/"+name+"/last.txt","r")
            # lt=fl.read().strip() 
            # lst.remove("last.txt")
            # fl.close()
        # except:
            # lt=None
        # wall=random.choice(lst)
        # while wall==lt:
            # wall=random.choice(lst)
        # fl=open("/root/Pictures/Wallpapers/"+nam+"/last.txt","w")
        # fl.write(wall)
        # fl.close()
        # path="/root/Pictures/Wallpapers/"+nam+"/"+wall
        # set_wall(path)
        # time.sleep(dic["period"])
