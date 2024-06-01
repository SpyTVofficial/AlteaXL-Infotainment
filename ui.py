from tkinter import *
import time
import os
from PIL import ImageTk, Image
from radio import get_radio_stations, play_radio, pause_radio, player

def create_main_window():
    # Main window
    win = Tk()
    win.configure(bg='black')
    win.geometry('800x600')  # Set the window size to 800x600
    win.attributes('-fullscreen', True)

    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Load image
    car_image = Image.open(os.path.join(current_dir, "images/car_front.png"))
    car_image = car_image.resize((50, 50))  # Resize the image
    car_image = ImageTk.PhotoImage(car_image)

    # Load back button image
    back_image_path = os.path.join(current_dir, "images/back.png")
    back_image = Image.open(back_image_path)
    back_image = back_image.resize((50, 50))  # Resize to 50x50 pixels
    back_image = ImageTk.PhotoImage(back_image)

    # Time label
    font_size = 25
    time_label = Label(win, bg='black', fg='white', font=('Roboto', font_size))
    time_label.grid(row=0, column=1, sticky='w')  # Adjust column

    # Frames for the menus and volume control
    frame1 = Frame(win, bg='grey', width=250, height=250)
    frame2 = Frame(win, bg='grey', width=250, height=250)
    frame3 = Frame(win, bg='grey', width=250, height=250)
    frame1.grid(row=1, column=1, sticky='nsew')  # Adjust column
    frame2.grid(row=1, column=2, sticky='nsew')
    frame3.grid(row=1, column=3, sticky='nsew')

    # Screen state
    screen_state = True
    is_playing = False  # Initialize is_playing

    def toggle_screen():
        nonlocal screen_state, is_playing
        screen_state = not screen_state
        if screen_state:
            frame1.grid(row=1, column=1, sticky='nsew')
            frame2.grid(row=1, column=2, sticky='nsew')
            frame3.grid(row=1, column=3, sticky='nsew')
            volume_slider.grid(row=0, column=0, rowspan=4, sticky='ns')  # Span the entire height
            time_label.grid(row=0, column=1, sticky='w')
            onoff_label.grid(row=0, column=3, sticky='e')
            car_label.grid(row=3, column=3, sticky='se')  # Place car image at bottom right
            if is_playing:  # If the radio was playing before the screen was turned off, resume playing
                toggle_play_pause()
        else:
            frame1.grid_remove()
            frame2.grid_remove()
            frame3.grid_remove()
            volume_slider.grid_remove()
            time_label.grid_remove()
            car_label.grid_remove()  # Remove car image when screen is off
            if is_playing:  # If the radio is playing, pause it
                toggle_play_pause()

    # Load and resize on/off image
    onoff_image_path = os.path.join(current_dir, "images/onoff.webp")
    onoff_image = Image.open(onoff_image_path)
    onoff_image = onoff_image.resize((50, 50))  # Resize to 50x50 pixels
    onoff_image = ImageTk.PhotoImage(onoff_image)

    # On/off image label
    onoff_label = Label(win, image=onoff_image, bg='black')
    onoff_label.grid(row=0, column=3, sticky='e')
    onoff_label.bind("<Button-1>", lambda e: toggle_screen())

    # Car image label
    car_label = Label(win, image=car_image, bg='black')
    car_label.grid(row=3, column=3, sticky='se')  # Place car image at bottom right
    car_label.bind("<Button-1>", lambda e: open_car_information_menu())

    # Volume Slider
    def set_volume(val):
        volume = int(val)
        player.audio_set_volume(volume)

    volume_slider = Scale(win, from_=100, to=0, orient=VERTICAL, bg='black', fg='white', highlightbackground='black', troughcolor='grey', command=set_volume)
    volume_slider.set(50)  # Default volume set to 50%
    volume_slider.grid(row=0, column=0, rowspan=4, sticky='ns')  # Use grid with rowspan to stretch

    # Radio station data
    radio_stations = get_radio_stations()
    radio_images = {
        "Eldoradio": os.path.join(current_dir, "images/eldoradio.png"),
        "RTL.lu": os.path.join(current_dir, "images/rtl.png")
    }

    # Canvas to display radio station name and logo
    canvas = Canvas(frame2, bg='grey', width=250, height=180)
    canvas.pack(pady=20)

    # Load pause icon
    image_path = os.path.join(current_dir, "images/pause_icon.png")
    pause_icon = ImageTk.PhotoImage(Image.open(image_path))

    # Load images
    radio_logos = {name: ImageTk.PhotoImage(Image.open(img)) for name, img in radio_images.items()}

    def display_radio_station(index):
        canvas.delete("all")
        station_name = radio_stations[index]
        logo = radio_logos[station_name]
        canvas.create_text(125, 20, text=station_name, fill="white", font=('Roboto', 15))
        canvas.create_image(125, 120, image=logo)
        canvas.image = logo  # Keep a reference to prevent garbage collection

        # Play the radio station
        play_radio(station_name)
        nonlocal is_playing
        is_playing = True

    def toggle_play_pause(event=None):
        nonlocal is_playing
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
        nonlocal current_station_index, is_playing
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
    current_station_index = 0  # Ensure this variable is defined
    display_radio_station(current_station_index)

    # Car Information Menu
    def open_car_information_menu():
        car_label.grid_remove()  # Remove car label from main menu

        # Car Information Frame
        car_info_frame = Frame(win, bg='black')
        car_info_frame.place(relwidth=1, relheight=1)

        # Back button with image
        back_button = Button(car_info_frame, image=back_image, command=lambda: close_car_information_menu(car_info_frame), bg='black', borderwidth=0)
        back_button.pack(side=TOP, anchor=NW, pady=20, padx=20)

        # Create 5 blank menus
        for i in range(5):
            Label(car_info_frame, text=f"Menu {i + 1}", bg='black', fg='white', font=('Roboto', 25)).pack(pady=10)

        # Animate car icon to the top right corner
        animate_car_icon(car_info_frame)

    def animate_car_icon(car_info_frame):
        car_info_canvas = Canvas(car_info_frame, width=50, height=50, bg='black', highlightthickness=0)
        car_info_canvas.place(x=750, y=550)  # Initial position of the car icon

        car_icon = car_info_canvas.create_image(0, 0, anchor=NW, image=car_image)

        def move_icon():
            nonlocal car_info_canvas, car_icon
            x, y = car_info_canvas.coords(car_icon)
            if x > 10:
                car_info_canvas.move(car_icon, -10, -10)  # Move up-left
                car_info_frame.after(50, move_icon)  # Call move_icon every 50 ms
            else:
                car_info_canvas.place_forget()  # Remove the car icon canvas after animation

        move_icon()

    def close_car_information_menu(car_info_frame):
        car_info_frame.destroy()  # Close the car information menu
        car_label.grid(row=3, column=3, sticky='se')  # Restore car label to the main menu

    # Update time function
    def update_time():
        current_time = time.strftime('%H:%M')
        time_label.config(text=current_time)
        win.after(1000, update_time)

    def quit_win():
        win.destroy()

    update_time()
    win.mainloop()

if __name__ == "__main__":
    create_main_window()
