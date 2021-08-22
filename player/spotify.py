#!/usr/bin/env python3
import sys
import os
import math
import json
from pprint import pprint
from time import monotonic, time
import spotipy
import spotipy.util as util
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import requests


load_dotenv(verbose=True)
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")


class Spotify:

    def __init__(self):

        self.scope = "user-read-playback-state,user-modify-playback-state,user-library-modify,user-library-read"
        self.song = None
        self.timer = None
        self.countdown_ms = None
        self.is_playing = False
        self.is_heart = False
        self.aa = None
        self.sp = None

    def make_req(self):
        r = requests.get(f'https://accounts.spotify.com/authorize?client_id={SPOTIPY_CLIENT_ID}&response_type=code&redirect_uri={SPOTIPY_REDIRECT_URI}&scope={self.scope}',allow_redirects=True)

        print(r.url)
        print(r)
        # r = requests.get((r.history[0].headers['location']))
        r = requests.get(r.url)
        #print(r)
        #print(r.__dict__)
        #for resp in r.history:

        #    print(resp.headers['location'], resp.status_code, resp.url)
        exit()

    def login(self):
        self.make_req()
        auth = SpotifyOAuth(scope=self.scope, client_id=SPOTIPY_CLIENT_ID, redirect_uri=SPOTIPY_REDIRECT_URI, client_secret=SPOTIPY_CLIENT_SECRET)
        self.sp = spotipy.Spotify(auth_manager=auth)

    def update_countdown_percent(self):
        return self.update_countdown() / self.song['item']['duration_ms']

    def update_countdown(self):
        # return percent
        if self.is_playing:
            elapsed = self.song['progress_ms'] + \
                (int(round(time() * 1000)) - self.song['timestamp'])
        else:
            elapsed = self.song['progress_ms']

        return elapsed

    # , self.song['item']['duration_ms'], self.song['progress_ms'],
    # int(round(time() * 1000)), self.song['timestamp'],
    # (int(round(time() * 1000)) - self.song['timestamp'])

    def handle_input(self, inp):
        if inp == 'next':
            self.next_track()
        elif inp == 'prev':
            self.last_track()
        elif inp == 'play':
            if self.is_playing:
                self.pause()
            else:
                self.start()
        elif inp == 'heart':
            if self.is_heart:
                self.unlike_track()
            else:
                self.like_track()
        elif inp is not None:
            self.seek_track(float(inp))

    def like_track(self):
        self.sp.current_user_saved_tracks_add([self.song['item']['uri']])
        return self.get_track()

    def unlike_track(self):
        self.sp.current_user_saved_tracks_delete([self.song['item']['uri']])
        return self.get_track()

    def is_track_liked(self):
        self.is_heart = self.sp.current_user_saved_tracks_contains(
            [self.song['item']['uri']])[0]
        return self.is_heart

    def next_track(self):
        self.sp.next_track()
        return self.get_track()

    def last_track(self):
        self.sp.previous_track()
        return self.get_track()

    def pause(self):
        self.sp.pause_playback()
        return self.get_track()

    def start(self):
        self.sp.start_playback()
        return self.get_track()

    def seek_track(self, percent):
        # ms = monotonic() / 1000
        self.sp.seek_track(
            math.floor(self.song['item']['duration_ms'] * percent))
        # self.song['item']['duration_ms'] = math.floor(
        #     self.song['item']['duration_ms'] * percent +
        #     (ms - monotonic() / 1000))

    def get_track(self):
        self.song = self.sp.currently_playing()
        self.is_playing = self.song['is_playing']
        self.countdown_ms = self.song['item']['duration_ms'] - \
            self.song['progress_ms']
        self.is_track_liked()
        self.get_audio_analysis()
        return self.song['item']

    def get_audio_analysis(self):
        self.aa = self.sp.audio_analysis(self.song['item']['id'])
        return int(self.aa['track']['tempo'])

        # Change track
        # sp.start_playback(uris=['spotify:track:6gdLoMygLsgktydTQ71b15'])

        # Change volume
        # sp.volume(100)
        # sleep(2)
        # sp.volume(50)
        # sleep(2)
        # sp.volume(100)


# Spotify().seek_track(.5)
# s = Spotify()
