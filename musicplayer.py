from tkinter import*
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3 # Find the length of the song/audio
import tkinter.ttk as ttk

root=Tk()
root.title('Music Player')
root.iconbitmap(r'D:\Coding nd Software\PYTHON\mp3player\image\audio.ico')
root.geometry("500x350")

pygame.mixer.init()

def add_song():
  songs=filedialog.askopenfilenames(initialdir='audio/',title="Choose a song", filetypes=(("mp3 Files","*.mp3"),))
  for song in songs:
    song=song.replace("C:/Users/prasad/Music/Songs/", "")
    song=song.replace(".mp3", "")
    song_box.insert(END,song) 

def play():
  # set stopped var to false so the song can play when stop is pressed
  global stopped
  stopped=False
  song=song_box.get(ACTIVE)
  song=f'C:/Users/prasad/Music/Songs/{song}.mp3'

  pygame.mixer.music.load(song)
  pygame.mixer.music.play(loops=0)

  # call the play_time fn
  play_time()

  # update slider to position
  # slider_position=int(song_length)
  # my_slider.config(to=slider_position, value=0)

# playing all songs
def play_all():
  # next_one=song_box.curselection() # shows the current song playing in terms of Index
  # for i in next_one:
  #   next_one=next_one[i]
  #   song=song_box.get(next_one)
  #   song=f'D:/Coding nd Software/PYTHON/mp3player/audio/{song}.mp3'
  #   pygame.mixer.music.load(song)
  #   pygame.mixer.music.play(loops=0)
  #   i+=1
  pass
  
global stopped
stopped=False
def stop():
  # reset slider and status bar
  status_bar.config(text='')
  my_slider.config(value=0)
  pygame.mixer.music.stop()
  song_box.selection_clear(ACTIVE)

  # Clear the status bar
  status_bar.config(text='')

  # set stop var to true
  global stopped
  stopped=True

# create global pause var
global paused
paused=False
def pause(is_paused):
  global paused
  paused=is_paused

  if paused:
    pygame.mixer.music.unpause()
    paused=False
  else:
    pygame.mixer.music.pause()
    paused=True

def next_song():
  # reset slider and status bar
  status_bar.config(text='')
  my_slider.config(value=0)
  next_one=song_box.curselection() # shows the current song playing in terms of Index
  next_one=next_one[0]+1
  song=song_box.get(next_one)
  song=f'C:/Users/prasad/Music/Songs/{song}.mp3'

  pygame.mixer.music.load(song)
  pygame.mixer.music.play(loops=0)

  # clear active bar
  song_box.selection_clear(0,END)

  # move active bar
  song_box.activate(next_one)
  # Highlighting the next song
  song_box.selection_set(next_one, last=None)

def last_song():
  # reset slider and status bar
  status_bar.config(text='')
  my_slider.config(value=0)
  next_one=song_box.curselection() # shows the current song playing in terms of Index
  next_one=next_one[0]-1
  song=song_box.get(next_one)
  song=f'C:/Users/prasad/Music/Songs/{song}.mp3'

  pygame.mixer.music.load(song)
  pygame.mixer.music.play(loops=0)

  # clear active bar
  song_box.selection_clear(0,END)

  # move active bar
  song_box.activate(next_one)
  # Highlighting the next song
  song_box.selection_set(next_one, last=None)
  
def delete_song():
  stop()
  song_box.delete(ANCHOR)
  pygame.mixer.music.stop()

def delete_all_song():
  stop()
  song_box.delete(0,END)
  pygame.mixer.music.stop()

# song length and time info
def play_time():
  if stopped:
    return
  # grab current song time
  current_time=pygame.mixer.music.get_pos()/1000

  # throw up temp label to get data
  # slider_lab.config(text=f'Slider: {int(my_slider.get())} and Song Pos: {int(current_time)}')
  con_current_time=time.strftime('%H:%M:%S',time.gmtime(current_time))

  # current_song=song_box.curselection() # shows the current song playing in terms of Index
  song=song_box.get(ACTIVE)
  song=f'C:/Users/prasad/Music/Songs/{song}.mp3'

  # get song length with mutagen
  song_muta=MP3(song)
  global song_length
  song_length= song_muta.info.length
  # conv to time formate
  con_song_len=time.strftime('%H:%M:%S',time.gmtime(song_length))

  # increase curent time bt 1sec
  current_time+=1
  if int(my_slider.get()) == int(song_length):
    status_bar.config(text=f'Time Elapsed: {con_song_len} / {con_song_len}  ')
  elif paused:
    pass

  elif int(my_slider.get()) == int(current_time):
    # update slider to position
    slider_position=int(song_length)
    my_slider.config(to=slider_position, value=int(current_time))
  else:
    # update slider to position
    slider_position=int(song_length)
    my_slider.config(to=slider_position, value=int(my_slider.get()))
    con_current_time=time.strftime('%H:%M:%S',time.gmtime(int(my_slider.get())))
    status_bar.config(text=f'Time Elapsed: {con_current_time} / {con_song_len}  ')

    # move this thing along by 1 sec
    next_time=int(my_slider.get())+1
    my_slider.config(value=next_time)

  # status_bar.config(text=f'Time Elapsed: {con_current_time} / {con_song_len}  ')

  # update slider posti value to current postion
  # my_slider.config(value=int(current_time))
  
  # update time
  status_bar.after(1000,play_time)

# create slider

def slide(x):
  # slider_lab.config(text=f'{int(my_slider.get())} of {int(song_length)}')
  song=song_box.get(ACTIVE)
  song=f'C:/Users/prasad/Music/Songs/{song}.mp3'

  pygame.mixer.music.load(song)
  pygame.mixer.music.play(loops=0, start=int(my_slider.get()))


def volume(x):
  pygame.mixer.music.set_volume(volume_slider.get())
  # current_volume=pygame.mixer.music.get_volume()
  # slider_lab.config(text=current_volume)

# create master frame
master_frame=Frame(root)
master_frame.pack(pady=20)

#create playlist box

song_box=Listbox(master_frame,bg="white",fg="black",width=60,selectbackground="skyblue",selectforeground="black")
song_box.grid(row=0,column=0)


# Create play button Inages

back_img=PhotoImage(file='D:\Coding nd Software\PYTHON\mp3player\image\skip_pre.png')
forword_img=PhotoImage(file='D:\Coding nd Software\PYTHON\mp3player\image\skip_next.png')
play_img=PhotoImage(file='D:\Coding nd Software\PYTHON\mp3player\image\play.png')
pause_img=PhotoImage(file='D:\Coding nd Software\PYTHON\mp3player\image\pause.png')
stop_img=PhotoImage(file='D:\Coding nd Software\PYTHON\mp3player\image\stop.png')
lib_add_img=PhotoImage(file='D:\Coding nd Software\PYTHON\mp3player\image\lib_add.png')


#Create player control frame

controls_frame=Frame(master_frame)
controls_frame.grid(row=1,column=0,pady=20)

# create volume frame

volume_frame=LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0,column=1,padx=10)

# create player button
lib_add_btn=Button(controls_frame,image=lib_add_img,borderwidth=0,command=add_song).grid(row=0,column=0,padx=10)
back_btn=Button(controls_frame,image=back_img,borderwidth=0,command=last_song).grid(row=0,column=1,padx=10)
forword_btn=Button(controls_frame,image=forword_img,borderwidth=0,command=next_song).grid(row=0,column=5,padx=10)
play_btn=Button(controls_frame,image=play_img,borderwidth=0,command=play).grid(row=0,column=2,padx=10)
pause_btn=Button(controls_frame,image=pause_img,borderwidth=0,command=lambda:pause(paused)).grid(row=0,column=3,padx=10)
stop_btn=Button(controls_frame,image=stop_img,borderwidth=0,command=stop).grid(row=0,column=4,padx=10)

menu_bar=Menu(root)
root.config(menu=menu_bar)

fileMenu=Menu(menu_bar, tearoff=0)
# fileMenu.add_command(label="Play All",command=play_all)
# fileMenu.add_separator()
fileMenu.add_command(label="Add",command=add_song)
fileMenu.add_command(label="Delete",command=delete_song)
fileMenu.add_command(label="Delete All",command=delete_all_song)
menu_bar.add_cascade(label="Edit",menu=fileMenu)

# Status Bar
status_bar=Label(root,text='',bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=2)

# create song position slider
my_slider =ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2,column=0,pady=10)

# create volume slider
volume_slider =ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)

# create temp slider label
# slider_lab=Label(root,text='0')
# slider_lab.pack(pady=5)


root.mainloop()