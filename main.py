#!/usr/bin/env python3
import curses
import threading
import sched
from time import sleep, time, monotonic
from player.curses_object import Curse
from player.spotify import Spotify


class Main:

    def __init__(self):

        self.menu_items = ['Log In']
        self.curse_window = None
        self.curse_thread = None
        self.spotify = None
        self.spotify_scheduler = sched.scheduler(time, sleep)
        self.spotify_event = None
        self.spotify_thread = None

        self.start_spotify()

        self.run()

    def start_curses(self):
        return Curse()

    def start_spotify(self):
        self.spotify = Spotify()
        self.spotify.login()
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
        start_second = monotonic()
        self.curse_window = self.start_curses()
        k = 0
       #  mouse_arr = []
        self.curse_window.draw_boxes()
        while k != ord('q'):
            self.curse_window.print_info()

            # janky mouse crap because the getmouse func
            # doesn't work in gnome shell or ubuntu 18.04
            k = self.curse_window.stdscr.getch()

            if k == curses.KEY_MOUSE:
#                self.curse_window.log_scr.addstr(" " + str(k))
#                self.curse_window.log_scr.refresh()
                _, x, y, _, _ = curses.getmouse()
                self.curse_window.log_scr.addstr(str(self.curse_window.mouse_click(x, y)))
                self.curse_window.log_scr.refresh()
                # self.curse_window.log_scr.addstr(str(x) + ' ' + y)
            if (monotonic() - start_second) > 1:
                start_second = monotonic()
                self.curse_window.update_status_bar(
                    self.spotify.update_countdown())

#            if k != -1:
#                mouse_arr.append(k)
#            if k == ord('q') and len(mouse_arr) > 1:
#                k = None

       #     # janky mouse crap because the getmouse func
       #     # doesn't work in gnome shell or ubuntu 18.04
       #     if len(mouse_arr) == 6\
       #             and mouse_arr[0] == 27 and mouse_arr[1] == 91\
       #             and mouse_arr[2] == 77 and mouse_arr[3] == 35:
       #         # there was a mouse up event!
       #         mx = mouse_arr[4]
       #         my = mouse_arr[5]
       #         self.curse_window.mouse_click(mx, my)
       #         mouse_arr = []
       #     elif len(mouse_arr) >= 6:
       #         mouse_arr = []

        self.curse_window.kill()

        self.stop_scheduler_spotify()


if __name__ == '__main__':
    Main()
