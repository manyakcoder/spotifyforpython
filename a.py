import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API kimlik bilgileri
client_id = '*'
client_secret = '*'
redirect_uri = 'http://localhost:8080/callback'
scope = 'user-modify-playback-state user-library-modify user-read-currently-playing playlist-modify-public playlist-read-private user-top-read user-read-recently-played'

# Yetkilendirme işlemi
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

def pause_song():
    sp.pause_playback()

def next_song():
    sp.next_track()

def previous_song():
    sp.previous_track()

def like_song():
    current_track = sp.current_user_playing_track()
    if current_track is not None:
        track_id = current_track['item']['id']
        sp.current_user_saved_tracks_add(tracks=[track_id])
        print("Şarkı beğenildi!")
    else:
        print("Şu anda herhangi bir şarkı çalmıyor.")

def search_song():
    search_query = input("Aramak istediğiniz şarkı veya sanatçı adını girin: ")
    results = sp.search(q=search_query, type='track')
    tracks = results['tracks']['items']

    if len(tracks) > 0:
        print("Sonuçlar:")
        for i, track in enumerate(tracks):
            print(f"{i+1}. {track['name']} - {track['artists'][0]['name']}")

        choice = input("Oynatmak istediğiniz şarkının numarasını girin: ")
        try:
            track_index = int(choice) - 1
            track_uri = tracks[track_index]['uri']
            sp.start_playback(uris=[track_uri])
        except (ValueError, IndexError):
            print("Geçersiz seçenek!")
    else:
        print("Sonuç bulunamadı.")

def explore_popular_songs():
    results = sp.playlist('37i9dQZEVXbMDoHDwVN2tF')
    tracks = results['tracks']['items']

    if len(tracks) > 0:
        print("Popüler Şarkılar:")
        for i, track in enumerate(tracks):
            print(f"{i+1}. {track['track']['name']} - {track['track']['artists'][0]['name']}")
    else:
        print("Popüler şarkılar bulunamadı.")

def create_playlist():
    playlist_name = input("Oluşturmak istediğiniz çalma listesinin adını girin: ")
    playlist = sp.user_playlist_create(user=sp.me()['id'], name=playlist_name, public=True)
    print(f"{playlist_name} adında bir çalma listesi oluşturuldu.")
    print("Çalma listesi ID'si:", playlist['id'])

def add_song_to_playlist():
    playlist_id = input("Şarkıyı eklemek istediğiniz çalma listesinin ID'sini girin: ")
    search_query = input("Eklemek istediğiniz şarkının adını veya sanatçısını girin: ")
    results = sp.search(q=search_query, type='track')
    tracks = results['tracks']['items']

    if len(tracks) > 0:
        print("Sonuçlar:")
        for i, track in enumerate(tracks):
            print(f"{i+1}. {track['name']} - {track['artists'][0]['name']}")

        choice = input("Eklemek istediğiniz şarkının numarasını girin: ")
        try:
            track_index = int(choice) - 1
            track_uri = tracks[track_index]['uri']
            sp.playlist_add_items(playlist_id=playlist_id, items=[track_uri])
            print("Şarkı çalma listesine eklendi!")
        except (ValueError, IndexError):
            print("Geçersiz seçenek!")
    else:
        print("Sonuç bulunamadı.")

def show_currently_playing():
    current_track = sp.current_user_playing_track()
    if current_track is not None:
        track_name = current_track['item']['name']
        artist_name = current_track['item']['artists'][0]['name']
        progress_ms = current_track['progress_ms'] / 1000  # Convert milliseconds to seconds
        print(f"Şu anda çalıyor: {track_name} - {artist_name}")
        print(f"Geçen süre: {progress_ms} saniye")
    else:
        print("Şu anda herhangi bir şarkı çalmıyor.")

def show_user_playlists():
    playlists = sp.current_user_playlists()
    if len(playlists['items']) > 0:
        print("Çalma Listeleriniz:")
        for i, playlist in enumerate(playlists['items']):
            print(f"{i+1}. {playlist['name']} - ID: {playlist['id']}")
    else:
        print("Çalma listesi bulunamadı.")

def analyze_music_taste():
    top_artists = sp.current_user_top_artists(limit=5, time_range='medium_term')
    top_tracks = sp.current_user_top_tracks(limit=5, time_range='medium_term')

    if len(top_artists['items']) > 0:
        print("En Sevilen Sanatçılar:")
        for i, artist in enumerate(top_artists['items']):
            print(f"{i+1}. {artist['name']}")
        print()

    if len(top_tracks['items']) > 0:
        print("En Sevilen Şarkılar:")
        for i, track in enumerate(top_tracks['items']):
            print(f"{i+1}. {track['name']} - {track['artists'][0]['name']}")
    else:
        print("Müzik zevki bulunamadı.")

def show_recently_played():
    results = sp.current_user_recently_played(limit=50)
    if len(results['items']) > 0:
        print("Son Dinlenen Şarkılar:")
        for i, item in enumerate(results['items']):
            track = item['track']
            print(f"{i+1}. {track['name']} - {track['artists'][0]['name']}")
    else:
        print("Son dinlenen şarkı bulunamadı.")

# Ana döngü
while True:
    print("1. Şarkıyı duraklat")
    print("2. Şarkıyı atla")
    print("3. Şarkıyı geri sar")
    print("4. Şarkıyı beğen")
    print("5. Şarkı ara")
    print("6. Popüler şarkıları keşfet")
    print("7. Çalma listesi oluştur")
    print("8. Şarkıyı çalma listesine ekle")
    print("9. Şu anda çalan şarkıyı göster")
    print("10. Kullanıcı çalma listelerini göster")
    print("11. Müzik zevkimi analiz et")
    print("12. Son dinlenen şarkıları göster")
    print("0. Çıkış")
    choice = input("Seçiminizi yapın: ")

    if choice == '1':
        pause_song()
    elif choice == '2':
        next_song()
    elif choice == '3':
        previous_song()
    elif choice == '4':
        like_song()
    elif choice == '5':
        search_song()
    elif choice == '6':
        explore_popular_songs()
    elif choice == '7':
        create_playlist()
    elif choice == '8':
        add_song_to_playlist()
    elif choice == '9':
        show_currently_playing()
    elif choice == '10':
        show_user_playlists()
    elif choice == '11':
        analyze_music_taste()
    elif choice == '12':
        show_recently_played()
    elif choice == '0':
        break
    else:
        print("Geçersiz seçenek!")
