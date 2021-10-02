#!/usr/bin/env python3
import curses
import threading
import sched
import logging
import os
from time import sleep, time, monotonic, monotonic_ns
from player.curses_object import Curse
from player.spotify import Spotify


class stdOut:

    def __init__(self):
        if os.path.exists('out.log'):
            os.remove('out.log')
        logging.basicConfig(level=logging.INFO, filename='out.log')

    def write(self, txt):
        logging.info(txt)


class Main:

    def __init__(self):

        self.menu_items = ['Log In']
        self.curse_window = None
        self.curse_thread = None
        self.spotify = None
        self.spotify_scheduler = sched.scheduler(time, sleep)
        self.spotify_event = None
        self.spotify_thread = None
        self.log = stdOut()

        self.start_spotify()

        self.run()

    def start_curses(self):
        return Curse()

    def start_spotify(self):
        self.spotify = Spotify()
        self.spotify.login()
        track_info = self.spotify.get_track()

        if self.curse_window:
            self.curse_window.add_to_info_q(track_info)
        self.reset_spotify_thread()

    def reset_spotify_thread(self):
        self.spotify_thread = threading.Thread(name='spotipy_daemon',
                                               target=self.update_spotify_info,
                                               daemon=True)
        self.spotify_thread.start()

    def update_spotify_info(self):
        if not self.spotify:
            self.start_spotify()

        track_info = self.spotify.get_track()

        if self.curse_window:
            self.curse_window.add_to_info_q(track_info)

        self.stop_scheduler_spotify()

        if self.spotify.is_playing:
            self.spotify_event = self.spotify_scheduler.enter(
                self.spotify.countdown_ms / 1000 + .5, 1,
                self.update_spotify_info)
            self.spotify_scheduler.run()

    def stop_scheduler_spotify(self):
        if self.spotify_event and\
                self.spotify_event in self.spotify_scheduler.queue:
            self.spotify_scheduler.cancel(self.spotify_event)

    def run(self):
        k = 0

        start_second = monotonic()
        start_four_second = monotonic()
        start_ms = monotonic() * 1000
        track_info = None

        self.curse_window = self.start_curses()
        self.curse_window.draw_boxes()
        self.curse_window.print_info()
        self.curse_window.marquee()
        self.curse_window.update_heart_button(self.spotify.is_heart)

        while k != ord('q'):
            self.curse_window.print_info()

            k = self.curse_window.stdscr.getch()

            if k == curses.KEY_MOUSE:
                _, x, y, _, _ = curses.getmouse()
                inp = self.curse_window.mouse_click(x, y)
                if inp is not None:
                    self.spotify.handle_input(inp)
                    self.reset_spotify_thread()
                    self.curse_window.update_play_button(
                        not self.spotify.is_playing)

            if k == curses.KEY_RESIZE:
                self.curse_window.allscr.clear()
                self.curse_window.draw_boxes()

            if (monotonic() - start_four_second) > 1:
                start_four_second=monotonic()
                track_info = self.spotify.get_track()
            if (monotonic() - start_second) > 1:
                start_second = monotonic()
                self.curse_window.marquee()
                self.curse_window.update_status_bar(
                    self.spotify.update_countdown_percent())
                self.curse_window.update_heart_button(self.spotify.is_heart)

                if self.curse_window and track_info:
                    self.curse_window.add_to_info_q(track_info)


            if (monotonic() * 1000 - start_ms) > 100:
                start_ms = monotonic() * 1000
                if self.spotify.aa:
                    self.curse_window.draw_vis(self.spotify.update_countdown(),
                                               self.spotify.aa)
                # self.log.write(self.spotify.get_audio_analysis())

        self.curse_window.kill()

        self.stop_scheduler_spotify()


if __name__ == '__main__':
    Main()
