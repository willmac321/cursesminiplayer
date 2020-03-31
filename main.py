#!/usr/bin/env python3
import curses
import threading
from player.curses_object import Curse
from player.spotify import Spotify

class Main:

    def __init__(self):

        self.menu_items = ['Log In']
        self.curse_window = None
        self.curse_thread = None
        self.spotify_thread = None
        self.spotify_thread = Spotify()

        curses.wrapper(self.start_curses)

    def start_curses(self, stdscr):
        self.curse_window = Curse(stdscr)
        self.curse_thread = threading.Thread(
            name='curse_daemon',
            target=self.curse_window.run,
        )
        self.curse_thread.start()
        self.curse_window.add_to_title_q('aaaast')


if __name__ == '__main__':
    Main()
