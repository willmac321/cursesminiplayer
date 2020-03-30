#!/usr/bin/env python3

import sys
import os
import curses
import threading
import time
from player.curses_object import Curse


class Main:

    def __init__(self):
        self.menu_items = ['Log In']
        self.curse_window = None
        self.curse_thread = None
        curses.wrapper(self.start_curses)

    def start_curses(self, stdscr):
        self.curse_window = Curse(stdscr)
        self.curse_thread = threading.Thread(
            name='curse_daemon',
            target=self.curse_window.run,
        )
        self.curse_thread.start()
        time.sleep(1)
        self.curse_window.add_to_queue('aaaast')
        self.curse_window.add_to_queue('tesst')
        time.sleep(1)
        self.curse_window.add_to_queue('tesst')


if __name__ == '__main__':
    Main()
