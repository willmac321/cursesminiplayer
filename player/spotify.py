#!/usr/bin/env python3
import sys
import os
import spotipy
import spotipy.util as util
import math
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from time import sleep, monotonic

load_dotenv(verbose=True)
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPiY_REDIRECT_URI")


class Spotify:

    def __init__(self):

        self.scope = "user-read-playback-state,user-modify-playback-state"
        self.song = None
        self.timer = None
        self.countdown_ms = None
        self.is_playing = False

        if len(sys.argv) > 1:
            self.username = sys.argv[1]
        else:
            print("Usage: %s username" % (sys.argv[0],))
            sys.exit()

        token = util.prompt_for_user_token(self.username, self.scope)
        self.sp = spotipy.Spotify(auth=token)

        self.get_track()

    def next_track(self):
        self.sp.next_track()
        self.get_track()

    def last_track(self):
        self.sp.previous_track()
        self.get_track()

    def pause(self):
        self.sp.pause_playback()

    def start(self):
        self.sp.start_playback()
        self.get_track()

    def seek_track(self, percent):
        ms = monotonic() / 1000
        self.sp.seek_track(
            math.floor(self.song['item']['duration_ms'] * percent))
        self.song['item']['duration_ms'] = math.floor(
            self.song['item']['duration_ms'] * percent +
            (ms - monotonic() / 1000))

    def get_track(self):
        self.song = self.sp.currently_playing()
        pprint(self.song['item']['name'])
        self.is_playing = self.song['is_playing']
        self.countdown_ms = self.song['item']['duration_ms'] - \
            self.song['progress_ms']

        if not self.timer:
            self.timer = threading.Timer(
                self.countdown_ms / 1000 + .2, self.get_track)
        else:
            self.timer.Change(self.countdown_ms / 1000)

        pprint(self.timer)

        if self.is_playing:
            self.timer.start()
        pprint(self.timer)

        # Change track
        # sp.start_playback(uris=['spotify:track:6gdLoMygLsgktydTQ71b15'])

        # Change volume
        # sp.volume(100)
        # sleep(2)
        # sp.volume(50)
        # sleep(2)
        # sp.volume(100)


# Spotify().seek_track(.5)
s = Spotify()
