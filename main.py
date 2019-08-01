#!/bin/python3

import getpass
import re

import vk_api
import gmusicapi
from vk_api.audio import VkAudio

vk_session = vk_api.VkApi(input("VK user: "), getpass.getpass(prompt="VK password: "))
try:
    vk_session.auth()
except vk_api.AuthError as e:
    print(e)
    exit(1)

vkaudio = VkAudio(vk_session)
vk_song_list = []


def cleanup(str):
    str = re.sub(r'\([^)]*\)', '', str)
    str = re.sub(r'\[[^\]]*\]', '', str)
    str = re.sub(r'^[^\w]*', '', str)
    str = re.sub(r'[^\w]*$', '', str)
    return str


for track in vkaudio.get():
    artist = cleanup(track['artist'])
    title = cleanup(track['title'])
    song = artist + ' ' + title
    vk_song_list.append(song)

gapi = gmusicapi.Mobileclient()
creds = gapi.perform_oauth(open_browser=True)
if not gapi.oauth_login(gmusicapi.Mobileclient.FROM_MAC_ADDRESS, oauth_credentials=creds):
    print('Failed to login to google')
    exit(1)

vk_playlist_id = gapi.create_playlist('VK')

for song in vk_song_list:
    result = gapi.search(song, max_results=1)
    songs = result['song_hits']
    if len(songs) > 0:
        gapi.add_songs_to_playlist(vk_playlist_id, songs[0]['track']['storeId'])
    else:
        print('Song "%s" haven\'t been found' % song)
print('DONE')
exit(0)
