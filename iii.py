#importing modules
import tkinter as tk
from tkinter.ttk import *  #for creating gui
from pytube import YouTube, request  #yoututbe api and request for requseting iterable string
from tkinter.filedialog import *  #for messagebox
from tkinter.messagebox import *
from threading import * #for threading
from tkinter import Button #button widget
import requests #to download video 
import shutil #to move files
global path_to_save 
import os
import atexit
"""
function to download the video

"""
def one_more_thread():
    thread=Thread(target=one_more)
    thread.start()
def one_more():
    shutil.copy("iii.py","one_more.py")
    os.system('cmd /c"python one_more.py"')


def exit_function():
    os.remove("one_more.py")


if __name__ == '__main__':
    atexit.register(exit_function )

def down(link,itag):
        try:
            yt = YouTube(link)                     #accessing the particular video by link
            video=yt.streams.get_by_itag(itag)     #specify the quality by itag
            global is_paused, is_cancelled         
            videotitle=yt.title                    #fetching the title of the video
            filesize=video.filesize                #fetching the file size
            g=videotitle+'.mp4'                    
            with open(g, 'wb') as f:                #opening the file in write binary mode
                is_paused = is_cancelled = False
                video = request.stream(video.url)  # get an iterable stream
                downloaded = 0
                while True:
                    if is_cancelled:                #if the download is cancelled
                        button['state'] = 'normal'            #setting the button states
                        button['text']="Download"
                        pause_button['state'] = 'normal'
                        cancel_button['state'] = 'normal'
                        os.execl('iii.py', '')              #if cancelled then restarting the script
                        break
                    if is_paused:               #if paused
                        continue
                    chunk = next(video, None)  # get next chunk of video
                    if chunk:
                        f.write(chunk)              #writing  chunk to  the open file
                        downloaded += len(chunk)    #len(chunk) returns size of chunk
                        percent=((downloaded/filesize)*100)
                        button['text']="{:.2f}%downloaded".format(percent)
                    else:
                        # no more data
                       
                        break
            if(itag=='135' or itag=='137' or itag=='160' or itag=='242'): #these videos with these itags dont have sound therefore we download and add sound
                source_path=os.getcwd()+"\\"+g                              #path of the downloaded video
                dest_path=os.getcwd()+"\\"+"v.mp4"                          #renaming for simplicity in further code 
                os.rename(source_path,dest_path)                                           
                completedownload1080(link)                                     #calling completedownload1080
            else:
                 completedownload(link)                                 # for videos other than the above mentioned  calling complete download
                 button['state'] = 'normal'
                 button['text']="Download"
                 pause_button['state'] = 'normal'
                 cancel_button['state'] = 'normal'

        except :
                if(is_cancelled==True):
                    button['state'] = 'normal'                      #if the download fails except statement gets executed
                    pause_button['state'] = 'disabled'
                    cancel_button['state'] = 'disabled'
                    button['text'] = 'Download'
                    button['state'] = 'active'
                else: 
                    showinfo("Error","Check your internet connection")
                    button['state'] = 'normal'                      #if the download fails except statement gets executed
                    pause_button['state'] = 'disabled'
                    cancel_button['state'] = 'disabled'

                    button['text'] = 'Download'
                    button['state'] = 'active'

"""
function to move the downloaded file  to desired directory

"""
def move_to_destination(link):
    yt = YouTube(link)                          
    title=yt.title                              #get the title of video
    button['text']="processing.."               
    source_path=os.getcwd()+"\\"+title+".mp4"   #current location of downloaded file
    output=askdirectory()                       #taking user input for desired directory
    opath=output+"\\"+title+".mp4"              #path where the file should be moved
    shutil.move(source_path,opath)              #shutil.move moves the file to specified location

"""
function to pause download

"""
def toggle_download():
    global is_paused
    is_paused = not is_paused                          #changes is_paused=false to is_paused=true
    pause_button['text'] = 'Resume' if is_paused else 'Pause'  #changing button texts

"""
function to cancel the download

"""
def cancel_download():
    global is_cancelled
    is_cancelled = True  

"""
function to move the downloaded video and notify the user on 
download completion.
"""
def completedownload( link):
    move_to_destination(link)                               #calling the fuction declared earlier
    showinfo("Download completed", "video downloaded")      #message box
    button['text']='Download'                               
    button['state']='active'
    linkField.delete(0,END)                                 #deleting the entered link  upon completion of the process 

"""
function to move the downloaded  soundless video and notify the user on 
download completion.

"""
def completedownload1080(link):
    merge1080(link)                                         #calling merge1080 function
    showinfo("Download window", "video downloaded") 
    button['text']='Download'
    button['state']='active'
    linkField.delete(0,END)

"""
function to download the audio

"""
def startdownloadaudio(link):  
    try:
        from pytube import YouTube                #library to download video in mp3 format
        yt = YouTube(link)
        video=yt.streams.get_audio_only() #getting the first quality which fuction returns
        global is_paused, is_cancelled
        videotitle=yt.title                             #title of video
        filesize=video.filesize                         #file size
        g=videotitle+'.mp3'
        with open(g, 'wb') as f:                        #this is the same fuction that we used for video downloading just the extension is changed frommp4 to mp3
                is_paused = is_cancelled = False
                video = request.stream(video.url)  # get an iterable stream
                downloaded = 0
                while True:
                    if is_cancelled: 
                        break
                    if is_paused:
                        continue
                    chunk = next(video, None)  # get next chunk of video
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        percent=((downloaded/filesize)*100)
                        button['text']="{:.2f}%downloaded".format(percent)
                    else:
                        # no more data
                        source_path=os.getcwd()+"\\"+videotitle+".mp3"
                        output=askdirectory()
                        opath=output+"\\"+videotitle+".mp3"
                        shutil.move(source_path,opath)
                       
                        showinfo("Download completed", "video downloaded")
                        button['text']='Download'
                        button['state']='active'
                        linkField.delete(0,END)
                    
                        break

    except :
                showinfo("Error","Check your internet connection")
                button['state'] = 'normal'
                pause_button['state'] = 'disabled'
                cancel_button['state'] = 'disabled'
               
                button['text'] = 'Download'
                button['state'] = 'active'

"""
this function starts running if download 
button is pressed.

"""
def buttonclicked():
    try:
        button["text"]="please wait..."   #specify the button states
        button['state']='disabled'
        pause_button['state'] = 'normal'
        cancel_button['state'] = 'normal'
        olink="http"
        global link
        link=linkField.get()          #taking the link from entry box
        if link==" ":                  #if non url is provided then stop  
            return
        elif(link[0:4]!=olink):
            showinfo("Error","Enter a valid link")
            button["text"]="Download"   #specify the button states
            button['state']="normal"
            linkField.delete(0,"end")
            return
            
        elif(clicked.get()=="720p"):
            itag='22'                                           #itags are codes for the specific video quality
            thread=Thread(target=down,args=(link,itag,))        #creating a thread to solve window not responding problem
            thread.start()
        elif (clicked.get() == "1080p"):
            itag='137'
            thread = Thread(target=down, args=(link,itag,))
            thread.start()
        elif (clicked.get() == "480p"):
            itag='135'
            thread = Thread(target=down, args=(link,itag,))
            thread.start()
        elif(clicked.get()=="360p"):
            itag='18'
            thread = Thread(target=down, args=(link,itag,))
            thread.start()
        elif (clicked.get() == "240p"):
            itag='242'
            thread = Thread(target=down, args=(link,itag,))
            thread.start()
        elif (clicked.get() == "144p"):
            itag='160'
            thread = Thread(target=down, args=(link,itag,))
            thread.start()
        elif (clicked.get() == "mp3"):
            thread = Thread(target=startdownloadaudio, args=(link,))
            thread.start()
       
    except Exception as e:                                                                          #if error occurs
        Label(main,text=e,font=("Verdana",30,"bold"),bg="gray24",fg="orangered").pack(side=TOP)     #label in the gui about error

"""
function to add audio to 
soundless videos.

"""
def merge1080(link):
    
    from pytube import YouTube             #to download the sound in mp3 format
    yt = YouTube(link)
    title=yt.title
    video = yt.streams.get_audio_only()
    button['text']="processing.."
    video.download(filename="a")  
    os.rename("a.mp4","a.mp3")            #downloading the audio with file name as "a".

    """  this  below command appends the audio to the 
    previously downloaded soundless video file "v" 
    with the help of ffmpeg module and the output 
    is video.mp4 with sound """

    os.system('cmd /c" ffmpeg -i v.mp4 -i a.mp3 -c:v copy -c:a aac video.mp4"')   #code to execute cmd commands via this script 
    os.remove("v.mp4")                   #delete  the soundless video
    os.remove("a.mp3")                      #delete the downloaded audio file
    source_path=os.getcwd()+"\\"+"video.mp4" #current working directory
    output=askdirectory()                     #asking user for desired directory
    opath=output+"\\"+title+".mp4"
    shutil.move(source_path,opath)          #moving the file to the directory specified by the user

"""
function to quit

"""
def closewindow():
    main.destroy()                      #close tkinter window

"""
function which prints title ,thumbnail,viewcount
and rating of the video

"""
def info():
    
    link=linkField.get()                    #get the link from entry box
    newwindow=tk.Toplevel(main)                #create a new tkinter window
    newwindow.geometry("1000x1000")        #window size,title,icon
    newwindow.title("INFO")                       
    newwindow.iconbitmap("1.ico")
    headingicon1 = tk.Label(newwindow, image=file)
    headingicon1.place(x=0, y=0, relwidth=1, relheight=1)  #use the image as background
    loadingvar=tk.StringVar()     #to change the text of the label loading 
    loadingvar.set("Loading...")
    tk.Label(newwindow,font=('Verdana',20,"bold"),bg="gray24",fg="orangered",textvariable=loadingvar,borderwidth=0).pack(side="top",pady=15)
    yt = YouTube(link)
    z = yt.thumbnail_url                  #gettin gthe thumbnail url
    d= ("{:.2f}".format(yt.length / 60))  #assigning variables to length,views,title and rating of the video in two decimal place
    v = "{:.2f}".format(yt.views / 1000)
    m = "{:.2f}".format(yt.rating)
    t = yt.title
    image_url = z
    filename = "thumbnail.jpg"
    r = requests.get(image_url, stream=True) #get url
    if r.status_code == 200:                 #if this condition is not met we cannot download
        r.raw.decode_content = True        #read content in url
        with open(filename, 'wb') as f:   #write binary
            shutil.copyfileobj(r.raw, f)  #copy read content to thumbnail.jpg
    else:
        print('error')
    from PIL import ImageTk, Image      #to use  jpg images in tkinter 
    global img1
    path = filename
    img = Image.open(path)
    resized = img.resize((500, 425), Image.ANTIALIAS) #resize antialias is to resize if we dont mention it resize function crops out the thumnail image
    img1 = ImageTk.PhotoImage(resized)                #storing the image as photo image to use in tkinter
    loadingvar.set(t)
    tk.Label(newwindow,image=img1).pack(side="top",pady=20)  
    tk.Label( newwindow, text=("Duration:", d, "minutes"),font=('Verdana',30,"bold"),bg="gray24",fg="orangered",borderwidth=0).pack(side="top",pady=20)
    tk.Label(newwindow, text=("views:", v, "k"),font=('Verdana',30,"bold"),bg="gray24",fg="orangered",borderwidth=0) .pack(side="top",pady=20)
    tk.Label(newwindow, text=("Rating:", m, "out_of_5"),font=('Verdana',30,"bold"),bg="gray24",fg="orangered",borderwidth=0) .pack(side="top",pady=20)

""" thread to call info function """

def thread_for_info():
    infothread=Thread(target=info)
    infothread.start()
    
""" labels are used to display the content on tkinter window pack function is used to 
     specify the position of widgets with the help of padx and pady  buttons are used 
     to call functions ,entry box are used to take user input combo box are used to
     create dropdowns
"""
main=tk.Tk() 
main.title("YouTube video  downloader")
main.iconbitmap("1.ico")
main.geometry("1200x1200")
main.configure()
file=tk.PhotoImage(file="32819.png")
headingicon=tk.Label(main,image=file)

headingicon.place(x=0,y=0,relwidth=1,relheight=1)
tk.Label(main,text='enter the link ',font=('Verdana',30,"bold"),bg="gray24",fg="orangered",borderwidth=0).pack(side="top",pady=5)
linkField=tk.Entry(main,font=('Verdana',20,"bold"),justify="center",bg="gray24",fg="orangered")
linkField.pack(side="top",pady=5,ipadx=100)
linkField.focus()
tk.Label(main, text="choose the quality",font=('Verdana',30,"bold"),justify="center",bg="gray24",fg="orangered",borderwidth=0).pack(side="top",pady=5,padx=(0,18))
clicked=tk.StringVar()
clicked.set("720p")
v=['144p', '240p', '360p', '480p', '720p', '1080p','mp3']
combo=tk.OptionMenu(main,clicked,*v,)
combo.config(bg="gray24",fg="orangered",font=('verdana',20,'bold'))
combo["menu"].config(bg="gray24",fg="orangered",font=('verdana',20,'bold'))
combo.pack(side="top",pady=20,ipadx=20,ipady=5)
button=Button(main,text="Download",font=("Verdana",30,"bold"),bg="gray24",fg="orangered",command=buttonclicked,borderwidth=0)
button.pack(side="top",pady=5,ipadx=10)
cancel_button=Button(main,text="Cancel",font=("Verdana",30,"bold"),bg="gray24",fg="orangered",command= cancel_download,borderwidth=0)
cancel_button.pack(side="top",pady=5)
pause_button=Button(main,text="Pause",font=("Verdana",30,"bold"),bg="gray24",fg="orangered",command=toggle_download,borderwidth=0)
pause_button.pack(side="top",pady=5)
button2=Button(main,text="Info",font=("Verdana",30,"bold"),bg="gray24",fg="orangered",command= thread_for_info,borderwidth=0)
button2.pack(side="top",pady=5)
button1=Button(main,text="Quit",font=("Verdana",30,"bold"),bg="gray24",fg="orangered",command= closewindow,borderwidth=0)
button1.pack(side="top",pady=5)
button1=Button(main,text="one more",font=("Verdana",30,"bold"),bg="gray24",fg="orangered",command= one_more_thread,borderwidth=0)
button1.pack(side="top",pady=5)
main.mainloop()
