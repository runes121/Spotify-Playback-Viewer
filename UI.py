import sys
import traceback
import get_playdata
import io
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from urllib.request import urlopen
from plyer import notification

try:
    get_playdata.authenticate()
except Exception as e:
    print(f"Unhandled exception occurred while authenticating. {e}")

main_data = None

root = ttk.Window(themename="darkly", title="Current Playback")
root.geometry("800x400")


def process_img_web(main_data):
    album_art_bytes = urlopen(main_data["album_art_url"]).read()
    album_art_data = io.BytesIO(album_art_bytes)
    pil_album_art = Image.open(album_art_data)
    new_width = 200
    new_height = int(new_width * pil_album_art.height / pil_album_art.width)
    smaller_album_art = pil_album_art.resize((new_width, new_height))
    display_album_art = ImageTk.PhotoImage(smaller_album_art)
    return display_album_art


def process_img(img_location):
    img = Image.open(img_location)
    img = img.resize((30, 30))
    processed_img = ImageTk.PhotoImage(img)
    return processed_img


# Create variables to make global
album_art_label = None
title_text = None
artist_text = None
refresh_notify = None
device_name = None
is_paused_text = None
update_countdown = None
is_shuffling_icon = None
repeat_state_icon = None
last_album_art_url = ""


def display_data():
    global root
    global album_art_label
    global title_text
    global artist_text
    global device_name
    global is_paused_text
    global refresh_notify
    global update_countdown
    global is_shuffling_icon
    global last_album_art_url
    global repeat_state_icon

    try:
        main_data = get_playdata.get_main_data()
    except Exception as e:
        print(f"Unhandled exception occurred while getting play data. {e}")

    try:
        if main_data['is_playing']:
            print(main_data)
            # Display album art
            display_album_art = process_img_web(main_data)
            album_art_label = ttk.Label(root, image=display_album_art)
            album_art_label.image = display_album_art  # Prevent garbage collection
            album_art_label.pack()
            album_art_label.place(x=140, y=200, anchor="center")
            print("Done album label")

            # Display song title
            title_text = ttk.Label(root, font=("Arial", 20), text=main_data['track_name'])
            title_text.pack()
            title_text.place(x=260, y=100, anchor="nw")
            print("done song title")

            # Display artist name
            artist_text = ttk.Label(root, font=("Arial", 15), text=main_data['artist_names'])
            artist_text.pack()
            artist_text.place(x=260, y=150)
            print("done artist name")

            # Automatic refresh
            refresh_notify = ttk.Label(root, font=("Arial", 10), text="Data will refresh automatically.")
            refresh_notify.pack()
            print("done refresh")

            # Display device name
            device_name = ttk.Label(root, font=("Arial", 10), text=f"Playing on {main_data['playing_on']}")
            device_name.pack()
            device_name.place(x=260, y=280)
            print("done device name")

            # Display whether the song is paused
            is_paused_text = ttk.Label(root, font=("Arial Bold", 13), text=" ")
            is_paused_text.pack()
            is_paused_text.place(x=260, y=240)
            print("done pause")

            if main_data["is_paused"]:
                is_paused_text.configure(text="Paused.")
            print("configured paused")

            # Display update countdown
            update_countdown = ttk.Label(root, font=("Arial", 7), text="15")
            update_countdown.pack()
            print("done update countdown")

            # Display if the user is shuffling
            is_shuffling_icon = ttk.Label(root)
            is_shuffling_icon.image = process_img(f"{'shuffle_on.png' if main_data['shuffling'] else 'shuffle.png'}")
            is_shuffling_icon.configure(image=is_shuffling_icon.image)
            is_shuffling_icon.pack()
            is_shuffling_icon.place(x=260, y=185)
            print("done shuffling")

            # Display if the user is repeating
            repeat_state_icon = ttk.Label(root)
            if main_data["repeat_state"] == "off":
                repeat_state_icon.image = process_img("repeat.png")
            elif main_data["repeat_state"] == "track":
                repeat_state_icon.image = process_img("repeat_one_on.png")
            else:
                repeat_state_icon.image = process_img("repeat_on.png")

            repeat_state_icon.configure(image=repeat_state_icon.image)
            repeat_state_icon.pack()
            repeat_state_icon.place(x=295, y=185)

            return main_data["remaining_ms"]
        else:
            main_data = {
                "album_art_url": "https://avatars.cloudflare.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg"
            }
            last_album_art_url = main_data["album_art_url"]
            display_album_art = process_img_web(main_data)
            album_art_label = ttk.Label(root, image=display_album_art)
            album_art_label.image = display_album_art  # Prevent garbage collection
            album_art_label.pack()
            album_art_label.place(x=140, y=200, anchor="center")
            print("Done album label")

            # Display song title
            title_text = ttk.Label(root, font=("Arial", 20), text="No song is playing.")
            title_text.pack()
            title_text.place(x=260, y=100, anchor="nw")
            print("done song title")

            # Display artist name
            artist_text = ttk.Label(root, font=("Arial", 15), text=" ")
            artist_text.pack()
            artist_text.place(x=260, y=150)
            print("done artist name")

            # Automatic refresh
            refresh_notify = ttk.Label(root, font=("Arial", 10), text="Data will refresh automatically.")
            refresh_notify.pack()
            print("done refresh")

            # Display device name
            device_name = ttk.Label(root, font=("Arial", 10), text=f"Playing on...")
            device_name.pack()
            device_name.place(x=260, y=280)
            print("done device name")

            # Display whether the song is paused
            is_paused_text = ttk.Label(root, font=("Arial Bold", 13), text=" ")
            is_paused_text.pack()
            is_paused_text.place(x=260, y=240)
            print("done pause")

            # Display update countdown
            update_countdown = ttk.Label(root, font=("Arial", 7), text="5")
            update_countdown.pack()
            print("done update countdown")

            # Display if the user is shuffling
            is_shuffling_icon = ttk.Label(root)
            is_shuffling_icon.image = process_img("shuffle.png")
            is_shuffling_icon.configure(image=is_shuffling_icon.image)
            is_shuffling_icon.pack()
            is_shuffling_icon.place(x=260, y=185)
            print("done shuffling")

            # Display if the user is repeating
            repeat_state_icon = ttk.Label(root)
            repeat_state_icon.image = process_img("repeat.png")

            repeat_state_icon.configure(image=repeat_state_icon.image)
            repeat_state_icon.pack()
            repeat_state_icon.place(x=295, y=185)

            return "no_music_playing"
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exc()
        notification.notify(
            title="Error.",
            message="An unknown error occured while opening the application, please try again.",
            timeout=10
        )


time = 15


def update_countdown_timer():
    global time
    global update_countdown

    if time > 0:
        time -= 1
        update_countdown.configure(text=str(time))
    else:
        update_countdown.configure(text="Updating")

    root.after(1000, update_countdown_timer)


def update_data():
    global time
    global last_album_art_url
    print("updating")
    try:
        main_data = get_playdata.get_main_data()
    except Exception as e:
        print(f"Unhandled exception occurred while getting play data. {e}")
        root.after(10000, update_data)
        time = 10

    try:
        if main_data["is_playing"]:
            print(main_data)
            # Change album art
            if last_album_art_url != main_data["album_art_url"]:
                display_album_art = process_img_web(main_data)
                album_art_label.configure(image=display_album_art)
                album_art_label.image = display_album_art
                last_album_art_url = main_data["album_art_url"]


            # Change song title
            title_text.configure(text=main_data["track_name"])

            artist_text.configure(text=main_data['artist_names'])

            device_name.configure(text=f"Playing on {main_data['playing_on']}")

            is_shuffling_icon.image = process_img(f"{'shuffle_on.png' if main_data['shuffling'] else 'shuffle.png'}")
            is_shuffling_icon.configure(image=is_shuffling_icon.image)

            if main_data["is_paused"]:
                is_paused_text.configure(text="Paused.")
            else:
                is_paused_text.configure(text=" ")

            if main_data["repeat_state"] == "off":
                repeat_state_icon.image = process_img("repeat.png")
            elif main_data["repeat_state"] == "track":
                repeat_state_icon.image = process_img("repeat_one_on.png")
            else:
                repeat_state_icon.image = process_img("repeat_on.png")

            repeat_state_icon.configure(image=repeat_state_icon.image)

            if type(remaining_ms) is int:
                if main_data["remaining_ms"] < 15000:
                    print("refreshing at end of song")
                    root.after(main_data["remaining_ms"], update_data)
                    time = round(remaining_ms / 10000)
                else:
                    if main_data["is_paused"]:
                        print("refreshing in 5 seconds")
                        root.after(5000, update_data)
                        time = 5
                    else:
                        print("refreshing in 15 seconds")
                        root.after(15000, update_data)
                        time = 15
            else:
                print("refreshing in 15 seconds")
                root.after(15000, update_data)
                time = 15

        else:
            title_text.configure(text="No song is playing.")
            artist_text.configure(text="You are most likely listening to an ad.")
            is_shuffling_icon.configure(image=None)
            is_paused_text.configure(text=" ")
            main_data = {
                "album_art_url": "https://avatars.cloudflare.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg"
            }
            last_album_art_url = main_data["album_art_url"]
            album_art = process_img_web(main_data)
            album_art_label.configure(image=album_art)
            album_art.image = album_art
            time = 7
            root.after(7000, update_data)
    except UnboundLocalError:
        title_text.configure(text="No song is playing.")
        artist_text.configure(text="You are most likely listening to an ad.")
        is_shuffling_icon.configure(image=None)
        is_paused_text.configure(text=" ")
        main_data = {
            "album_art_url": "https://avatars.cloudflare.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg"
        }
        last_album_art_url = main_data["album_art_url"]
        album_art = process_img_web(main_data)
        album_art_label.configure(image=album_art)
        album_art.image = album_art
    except Exception as e:
        title_text.configure(text="An unknown error has occured.")
        artist_text.configure(text=str(e))
        main_data = {
            "album_art_url": "https://avatars.cloudflare.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg"
        }
        album_art = process_img(main_data)
        album_art_label.configure(image=album_art)
        album_art.image = album_art


remaining_ms = display_data()
if type(remaining_ms) is int:
    if remaining_ms < 15000:
        print("refreshing at end of song")
        root.after(remaining_ms, update_data)
        time = round(remaining_ms / 10000)
        update_countdown_timer()
    else:
        print("refreshing in 15 seconds")
        root.after(15000, update_data)
        time = 15
        update_countdown_timer()
elif remaining_ms == "no_music_playing":
    root.after(5000, update_data)
    time = 5
    update_countdown_timer()

root.mainloop()
