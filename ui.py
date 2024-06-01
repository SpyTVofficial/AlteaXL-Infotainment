from tkinter import *
import time
import os
from radio import get_radio_stations, play_radio, pause_radio, player

# Main window
win = Tk()
win.configure(bg='black')
win.attributes('-fullscreen', False)

# Time label
font_size = 25
time_label = Label(win, bg='black', fg='white', font=('Roboto', font_size))
time_label.pack(anchor='nw')

# Frames for the menus and volume control
frame1 = Frame(win, bg='grey', width=250, height=250)
frame2 = Frame(win, bg='grey', width=250, height=250)
frame3 = Frame(win, bg='grey', width=250, height=250)
frame1.pack(side='left', fill='both', expand=True)
frame2.pack(side='left', fill='both', expand=True)
frame3.pack(side='left', fill='both', expand=True)

# Volume Slider
def set_volume(val):
    volume = int(val)
    volume_label.config(text=f"Volume: {volume}%")
    player.audio_set_volume(volume)

volume_slider = Scale(win, from_=100, to=0, orient=VERTICAL, bg='black', fg='white', highlightbackground='black', troughcolor='grey', command=set_volume)
volume_slider.set(50)  # Default volume set to 50%
volume_slider.pack(side='left', fill='y', padx=20)

# Volume Label
volume_label = Label(win, bg='black', fg='white')
volume_label.pack(side='left', padx=5)

# First Menu: Empty
label1 = Label(frame1, text="Menu 1: Empty", bg='grey', fg='white')
label1.pack(pady=20)

# Second Menu: Radio
label2 = Label(frame2, text="Menu 2: Radio", bg='grey', fg='white')
label2.pack(pady=20)

# Radio station data
radio_stations = get_radio_stations()
radio_images = {
    "Eldoradio": "images/eldoradio.png",
    "RTL.lu": "images/rtl.png"
}

# Canvas to display radio station name and logo
canvas = Canvas(frame2, bg='grey', width=250, height=180)
canvas.pack(pady=20)

# Load pause icon
current_dir = os.path.dirname(__file__)
image_path = os.path.join(current_dir, "images", "pause_icon.png")
pause_icon = PhotoImage(file=image_path)

# Keep track of current station index and playing status
current_station_index = 0
is_playing = False

# Load images
radio_logos = {name: PhotoImage(file=os.path.join(current_dir, img)) for name, img in radio_images.items()}

def display_radio_station(index):
    canvas.delete("all")
    station_name = radio_stations[index]
    logo = radio_logos[station_name]
    canvas.create_text(125, 20, text=station_name, fill="white", font=('Roboto', 15))
    canvas.create_image(125, 120, image=logo)
    canvas.image = logo  # Keep a reference to prevent garbage collection
    canvas.logo = logo  # Keep a reference to prevent garbage collection

    # Play the radio station
    play_radio(station_name)
    global is_playing
    is_playing = True

def toggle_play_pause(event=None):
    global is_playing
    if is_playing:
        pause_radio()
        display_pause_icon()
    else:
        play_radio(radio_stations[current_station_index])
        remove_pause_icon()
    is_playing = not is_playing

def display_pause_icon():
    canvas.create_image(125, 120, image=pause_icon)
    canvas.image = pause_icon  # Keep a reference to prevent garbage collection
    canvas.create_rectangle(0, 0, 250, 180, fill='black', stipple='gray50')

def remove_pause_icon():
    display_radio_station(current_station_index)

def on_mouse_scroll(event):
    global current_station_index, is_playing
    if event.delta > 0:
        current_station_index = (current_station_index - 1) % len(radio_stations)
    else:
        current_station_index = (current_station_index + 1) % len(radio_stations)
    display_radio_station(current_station_index)
    if is_playing:  # Only restart playback if it was previously playing
        play_radio(radio_stations[current_station_index])

# Bind mouse scroll event to canvas
canvas.bind("<MouseWheel>", on_mouse_scroll)
canvas.bind("<Button-1>", toggle_play_pause)
canvas.focus_set()

# Display the first radio station
display_radio_station(current_station_index)

# Third Menu: Empty
label3 = Label(frame3, text="Menu 3: Empty", bg='grey', fg='white')
label3.pack(pady=20)

# Update time function
def update_time():
    current_time = time.strftime('%H:%M')
    time_label.config(text=current_time)
    win.after(1000, update_time)

def quit_win():
    win.destroy()

update_time()
win.mainloop()
