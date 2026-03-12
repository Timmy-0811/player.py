import tkinter as tk
import pygame
import random
import os
import keyboard
from pathlib import Path
import sys

# --- Init ---
pygame.mixer.init()

volume = 0.05
pygame.mixer.music.set_volume(volume)
current_song = None
paused = False
mp3s = []
dir = "<none>"

def play_random():
    global current_song, mp3s, dir
    pygame.mixer.music.stop()
    if not dir == "<none>":
        print(f"[DEBUG] list.check '{mp3s}'")

        if not dir == "all":
            if not mp3s:
                music_path = Path(f"./{dir}")
                mp3s = list(music_path.glob("*.mp3"))
                print(f"[DEBUG] list.new '{mp3s}'")
        else:
            if not mp3s:
                for i, ordner in enumerate(unterordner):
                    print(f"[DEBUG] list.all.scan '{ordner}'")
                    music_path = Path(f"./{ordner}")
                    mp3s = list(music_path.glob("*.mp3")) + mp3s
                print(f"[DEBUG] list.all.new '{mp3s}'")

        if not mp3s:
            print(f"[WARN] list.new.no_files '{dir}'")
            label.config(text="No Files!")
            return
            
        filename = random.choice(mp3s)
        if not os.path.exists(filename):
            print(f"[WARN] play.not_found '{filename}'")
            label.config(text=f"{filename} not found!")
            mp3s.remove(filename)
            root.after(1000, check_music)
            return
        current_song = filename
        mp3s.remove(filename)
        pygame.mixer.music.load(filename)
        if len(filename.name.removesuffix(".mp3")) >= 35:
            label.config(text=f"{filename.name.removesuffix('.mp3')[:33]}...")
        else:
            label.config(text=filename.name.removesuffix('.mp3'))
        pygame.mixer.music.play()
        if paused:
            pygame.mixer.music.pause()


def check_music():
    if not paused and not pygame.mixer.music.get_busy():
        play_random()
    root.after(500, check_music)

def set_volume(delta):
    global volume
    volume = max(0.0, min(1.0, volume + delta / 100))
    pygame.mixer.music.set_volume(volume)
    volume_num.config(text=f"{volume * 100:.1f}%")

def pause_music():
    global paused
    paused = not paused
    if paused:
        pygame.mixer.music.pause()
        pause_button.config(text="Resume")
    else:
        pygame.mixer.music.unpause()
        pause_button.config(text="Pause")

# --- hier wichtige sachen für ordner ---

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

unterordner = [
    name for name in os.listdir(BASE_DIR)
    if os.path.isdir(os.path.join(BASE_DIR, name))
]

def ordner_gewaehlt(name):
    label.config(text="Ready")
    global dir
    dir = name
    ausgewaehlter_ordner.set("from " + name)
    print(f"[DEBUG] list.choosen '{name}'")
    newlist()
    if name == "<none>":
        ausgewaehlter_ordner.set("Choose Playlist")

def newlist():
    global mp3s
    if not dir == "<none>":
        print(f"[DEBUG] list.choosen.dir './{dir}'")
    mp3s = []
    play_random()

list_visible = True

def toggle_lists():
    global list_visible
    list_visible = not list_visible
    if list_visible:
        button_frame.pack_forget()
        button_more_text.set("Show Playlists")
        root.geometry("300x180")
    else:
        button_frame.pack(pady=5)
        button_more_text.set("Hide Playlists")
        y = 220 + 21 * len(unterordner)
        root.geometry(f"300x{y}")

# --- UI ---
root = tk.Tk()
root.overrideredirect(True)
root.geometry("300x180")
root.attributes('-topmost', True)
root.configure(bg='#020052')

label = tk.Label(root, text="Ready", font=("Arial", 12), fg="#5EC900")
label.configure(bg='#020052')
label.pack(pady=(6, 0))

ausgewaehlter_ordner = tk.StringVar()
ausgewaehlter_ordner.set("Choose Playlist")
Playlist = tk.Label(root, textvariable=ausgewaehlter_ordner, font=("Arial", 8), fg="#5EC900")
Playlist.configure(bg='#020052')
Playlist.pack(pady=5)

volume_frame = tk.Frame(root)
volume_frame.configure(bg='#020052')
volume_frame.pack(pady=2)

volume_min = tk.Button(volume_frame, text="-5", fg="#5EC900", command=lambda: set_volume(-5))
volume_min.configure(bg='#020052')
volume_min.pack(side=tk.LEFT, padx=3)

volume_min = tk.Button(volume_frame, text="-1", fg="#5EC900", command=lambda: set_volume(-1))
volume_min.configure(bg='#020052')
volume_min.pack(side=tk.LEFT, padx=3)

volume_min = tk.Button(volume_frame, text="-0.2", fg="#5EC900", command=lambda: set_volume(-0.2))
volume_min.configure(bg='#020052')
volume_min.pack(side=tk.LEFT, padx=3)

volume_num = tk.Label(volume_frame, text="5.0%", fg="#5EC900", font=("Arial", 10))
volume_num.configure(bg='#020052')
volume_num.pack(side=tk.LEFT, padx=1)

volume_plus = tk.Button(volume_frame, text="+0.2", fg="#5EC900", command=lambda: set_volume(0.2))
volume_plus.configure(bg='#020052')
volume_plus.pack(side=tk.LEFT, padx=3)

volume_plus = tk.Button(volume_frame, text="+1", fg="#5EC900", command=lambda: set_volume(1))
volume_plus.configure(bg='#020052')
volume_plus.pack(side=tk.LEFT, padx=3)

volume_plus = tk.Button(volume_frame, text="+5", fg="#5EC900", command=lambda: set_volume(5))
volume_plus.configure(bg='#020052')
volume_plus.pack(side=tk.LEFT, padx=3)

button_frame = tk.Frame(root)
button_frame.configure(bg='#020052')
button_frame.pack(pady=15)

skip_button = tk.Button(button_frame, text="Skip", fg="#5EC900", command=play_random)
skip_button.configure(bg='#020052')
skip_button.pack(side=tk.LEFT, padx=5)

pause_button = tk.Button(button_frame, text="Pause", fg="#5EC900", command=pause_music)
pause_button.configure(bg='#020052')
pause_button.pack(side=tk.LEFT, padx=5)

exit_button = tk.Button(button_frame, text="Exit", fg="#5EC900", command=lambda: sys.exit(0))
exit_button.configure(bg='#020052')
exit_button.pack(side=tk.LEFT, padx=5)

button_more_text = tk.StringVar()
button_more_text.set("Hide Playlists")
more_button = tk.Button(root, textvariable=button_more_text, fg="#5EC900", bg='#020052', command=toggle_lists)
more_button.pack()

# --- ordner stuff ---

button_frame = tk.Frame(root)
button_frame.configure(bg='#020052')
button_frame.pack(pady=5)

tk.Button(
        button_frame,
        text="All",
        width=15,
        command=lambda name="all": ordner_gewaehlt(name),
        bg='#020052',
        fg="#5EC900"
    ).grid(row=1, column=0, padx=5, pady=5)

tk.Button(
        button_frame,
        text="None",
        width=15,
        command=lambda name="<none>": ordner_gewaehlt(name),
        bg='#020052',
        fg="#5EC900"
    ).grid(row=1, column=1, padx=5, pady=5)

for i, ordner in enumerate(unterordner):
    print(f"[DEBUG] folders.name '{ordner}'")
    if not ordner == "all":
        zeile = (i // 2) + 2
        spalte = i % 2
        tk.Button(
            button_frame,
            text=ordner,
            width=15,
            command=lambda name=ordner: ordner_gewaehlt(name),
            bg='#020052',
            fg="#C9AE00"
        ).grid(row=zeile, column=spalte, padx=5, pady=5, sticky="w")
    else:
        print("[ERROR] folders.name.invalid")
        print("############################")
        print("#   Your Folder Name is invalid!    #")
        print("#       It wont show up in GUI!        #")
        print("#          This is not an Error!           #")
        print("############################")


visible = True

def toggle_window():
    global visible
    if visible:
        root.withdraw()
        visible = False
    else:
        root.deiconify()
        root.update_idletasks()

        width = root.winfo_width()
        height = root.winfo_height()

        x = root.winfo_pointerx() - width // 2
        y = root.winfo_pointery() - height // 2

        root.geometry(f"+{x}+{y}")
        visible = True

toggle_lists()
check_music()

#Hotkeys
keyboard.add_hotkey("alt+0", lambda: toggle_window())
keyboard.add_hotkey("shift+alt+0", lambda: pause_music())
keyboard.add_hotkey("shift+alt+up", lambda: set_volume(1))
keyboard.add_hotkey("shift+alt+down", lambda: set_volume(-1))

root.mainloop()

