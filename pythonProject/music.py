#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title('MP3 PLAYER')
# root.iconbitmap('') --> En son bir icon ekle
root.geometry("600x450")

# Pygame başlatır.
pygame.mixer.init()

# ŞArkı uzunluğunun bilgisini alıyoruz.
def play_time():
    if stopped:
        return
    # Şarkının anlık süresi (Şimdiki zaman)
    current_time = pygame.mixer.music.get_pos() / 1000
    # Zaman formatına çeviriyoruz.
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    # Çalma listesinden şarkı başlığını al
    song = song_box.get(ACTIVE)
    # Şarkı başlığına dizin yapısı ve MP3 ekliyoruz.
    song = f'/home/duhan/Desktop/PythonProject/pythonProject/music/{song}.mp3'
    # MUTAGEN kütüphanesini kullanarak şarkımızı yüklüyoruz.
    song_mut = MP3(song)
    # Müzik boyutunu döndürüyoruz
    global song_length
    song_length = song_mut.info.length
    # Zaman formatına çeviriyoruz.
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    # Şimdiki zaman sürekli 1 sn artıyor. (song_length e eşit olana kadar böyle devam edecek)
    current_time += 1

# Slider yani kaydrıcı ile oynanıp oynanmadığını kontrol ediyoruz. (Video ileri veya geri alındı mı?)
    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length} ')
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        # Eğer kaydırıcının yeri ile oynanmadıysa
        # Value olarak şimdiki zaman (current_time) dönüyor.
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))
    else:
        # Eğer kaydırıcının yeri ile oynandıysa
        # My_slider yani benim ayarladığım dönüyor.
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))

        # Yeni zamanımızı time formatına çeviriyoruz.
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

        # Son durumda çıkış
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length} ')

        # Yeni Slider i her saniye +1 ekleyerek devam ettireceğiz.
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    status_bar.after(1000, play_time)

# Müzik ekleme fonksiyonu
def add_song():
    song = filedialog.askopenfilename(initialdir='music/', title="Choose a Song", filetypes=(("mp3 Files","*.mp3"), ))
    # Şarkı adından dizin bilgisi ve .mp3 uzantısı çıkarılmalı. (Sadece şarkı adı kalmalı)
    song=song.replace("/home/duhan/Desktop/PythonProject/pythonProject/music/", "")
    song=song.replace(".mp3", "")
    # Müzik listemizi ekleniyor.
    print(song)
    song_box.insert(END, song)

# Rock müzikler eklemek için kısayol
def add_rock_songs():
    songs = filedialog.askopenfilenames(initialdir='music/Rock', title="Choose a Song", filetypes=(("mp3 Files", "*.mp3"),))

    for song in songs:
        song = song.replace("/home/duhan/Desktop/PythonProject/pythonProject/music/", "")
        song = song.replace(".mp3", "")
        # Müzik playliste eklenir.
        song_box.insert(END, song)

# Rap müzikler eklemek için kısayol
def add_rap_songs():
    songs = filedialog.askopenfilenames(initialdir='music/Rap', title="Choose a Song", filetypes=(("mp3 Files", "*.mp3"),))

    for song in songs:
        song = song.replace("/home/duhan/Desktop/PythonProject/pythonProject/music/", "")
        song = song.replace(".mp3", "")
        # Müzik playliste eklenir.
        song_box.insert(END, song)

# Pop müzikler eklemek için kısayol.
def add_pop_songs():
    songs = filedialog.askopenfilenames(initialdir='music/Pop', title="Choose a Song", filetypes=(("mp3 Files", "*.mp3"),))

    for song in songs:
        song = song.replace("/home/duhan/Desktop/PythonProject/pythonProject/music/", "")
        song = song.replace(".mp3", "")
        # Müzik playliste eklenir.
        song_box.insert(END, song)

                # Seçilen şarkıyı oynatan fonksiyon
def play():
    # Şarkının çalabilmesi için durdurulan değişkeni FALSE olarak ayarlıyoruz.
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song = f'/home/duhan/Desktop/PythonProject/pythonProject/music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Şarkının uzunluğunu öğrenebilmek için play_time çağırıyoruz.
    play_time()

global stopped
stopped = False

# Mevcut çalan şarkıyı durdurmak için STOP fonksiyonu.
def stop():
    # Kaydırıcı ve durum çubuğunu sıfırlar.
    status_bar.config(text='')
    my_slider.config(value=0)
    # Şarkının çalmasını durdurur.
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    # Status bar temizlenir. (Müzik isimlerinin yazdığı liste)
    status_bar.config(text='')

    # STOP değişkenini true olarak ayarla. (Stopped TRUE, yani stop durumunda)
    global stopped
    stopped = True

# Çalma listesinde bulunan sonraki şarkı çalmaya başlar.
def next_song():
    # Slider ve Status bar sıfırlanır. (Kaydırıcı ve durum çubuğu)
    status_bar.config(text='')
    my_slider.config(value=0)

    # Geçerli şarkının numarası alınır.
    next_one = song_box.curselection()
    # Geçerli şarkı numarasını +1 eklenir. Yani sonraki şarkıya geçilir.
    next_one = next_one[0]+1
    # Çalma listesinden şarkı başlığı alınır.
    song = song_box.get(next_one)
    # Şarkının dosya yolu
    song = f'/home/duhan/Desktop/PythonProject/pythonProject/music/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Çalma listesi liste kutusundaki yeni aktif çubuk. (0 dan başlar)
    song_box.selection_clear(0, END)

    # Yeni Song bar aktif edilir.
    song_box.activate(next_one)

    # Aktif çubuk sonraki şarkıya ayarlanır.
    song_box.selection_set(next_one, last=None)

# Çalma listesinde bulunan bir önceki şarkının çalmasını sağlar.
def previous_song():
    # Slider ve Status bar resetlenir.
    status_bar.config(text='')
    my_slider.config(value=0)

    # Geçerli şarkının numarası alınır.
    previous_one = song_box.curselection()
    # Şarkının numarasından bir çıkarılır (Yani bir önceki şarkının numarası kaydedilir.)
    previous_one = previous_one[0] - 1
    # Çalma listesinden şarkı başlığını al
    song = song_box.get(previous_one)
    # Şarkının dosya yolu
    song = f'/home/duhan/Desktop/PythonProject/pythonProject/music/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Çalma listesi liste kutusundaki yeni aktif çubuk. (0 dan başlar)
    song_box.selection_clear(0, END)

    # Yeni Song bar aktif edilir.
    song_box.activate(previous_one)

    # Aktif çubuk sonraki şarkıya ayarlanır.
    song_box.selection_set(previous_one, last=None)

# Müzik silme fonksiyonu
def delete_song():
    stop()
    # Şu anda seçili şarkıyı sil
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

# Şarkı listesindeki tüm şarkıları siler.
def delete_all_songs():
    stop()
    # Bütün şarkıları sil.
    song_box.delete(0, END)
    # Eğer çalan bir müzik varsa o durdurulur.
    pygame.mixer.music.stop()

# Genl duraklama değişkeni FALSE ayarlandı.
global paused
paused = False

# Mevcut şarkıyı duraklat veya yeniden başlat.
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # Pause
        pygame.mixer.music.pause()
        paused = True

# Kaydırıcı (Müziği ileri veya geri almamızı sağlar.)
def slide(x):

    song = song_box.get(ACTIVE)
    song = f'/home/duhan/Desktop/PythonProject/pythonProject/music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

# Ses fonksiyonu
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    # Mevcut ses seviyesini al.
    current_volume = pygame.mixer.music.get_volume()

# Ses ayarlama çerçevesi.
master_frame = Frame(root)
master_frame.pack(pady=20)


# Playlist kutusu oluştur.
song_box = Listbox(master_frame, bg="BLACK", fg="GREEN", width=60, selectbackground="GRAY", selectforeground="BLACK")
song_box.grid(row=0, column=0)

# Kullanıcı kontrol iconları (Başlat, durdur vs.)
back_btn_img = PhotoImage(file = "/home/duhan/Desktop/PythonProject/pythonProject/icon/prevButton.png")
forward_btn_img = PhotoImage(file = "/home/duhan/Desktop/PythonProject/pythonProject/icon/nextButton.png")
play_btn_img = PhotoImage(file = "/home/duhan/Desktop/PythonProject/pythonProject/icon/startButton.png")
pause_btn_img = PhotoImage(file = "/home/duhan/Desktop/PythonProject/pythonProject/icon/pauseButton.png")
stop_btn_img = PhotoImage(file = "/home/duhan/Desktop/PythonProject/pythonProject/icon/stopButton.png")

# Kontrol çerçevesi
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=20)

# Ses çerçevesi
volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

# Player control butonları
back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0,column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4,padx=10)

my_menu = Menu(root)
root.config(menu=my_menu)

# Müzik ekleme menüsü
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs",menu=add_song_menu)
add_song_menu.add_command(label="Ad One Song TO Playlist", command=add_song)

# Müzik türüne göre kısayol menüleri
add_song_menu.add_command(label="Add rock music to playlist", command=add_rock_songs)
add_song_menu.add_command(label="Add rap music to playlist", command=add_rap_songs)
add_song_menu.add_command(label="Add pop music to playlist", command=add_pop_songs)
# Müzik silme menüsü
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)

# Müzik ileri geri alma çubuğu
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Müzik konumu kaydırıcı
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)

# Ses
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)



root.mainloop()