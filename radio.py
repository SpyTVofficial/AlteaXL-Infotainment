import vlc

# Define a VLC instance
vlc_instance = vlc.Instance()

# Create a player object
player = vlc_instance.media_player_new()

# Define radio stations and their stream URLs
radio_stations = {
    "Eldoradio": "https://stream.eldo.lu/data/live/radio/eldo/playlist.m3u8",
    "RTL.lu": "https://live-edge.rtl.lu/radio/rtl/playlist.m3u8"
}

current_station = None

def get_radio_stations():
    return list(radio_stations.keys())

def play_radio(station_name):
    global current_station
    if current_station != station_name:
        current_station = station_name
        stream_url = radio_stations[station_name]
        media = vlc_instance.media_new(stream_url)
        player.set_media(media)
    player.play()
    is_playing = True

def pause_radio():
    if player.is_playing():
        player.pause()

def stop_radio():
    player.stop()
