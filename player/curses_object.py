#!/usr/bin/env python3
import curses
import enum
from collections import deque
# from curses.textpad import Textbox, rectangle


class Color(enum.Enum):
    background = 1
    text = 2


class Curse:

    def __init__(self, stdscr):
        self.song_name_q = deque()
        self.y = 1
        self.x = 1
        curses.noecho()

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()

        stdscr.refresh()

        # Start colors in curses
        curses.start_color()

        # these are for UI
        curses.init_pair(Color.background.value, curses.COLOR_CYAN,
                         curses.COLOR_BLACK)
        curses.init_pair(Color.text.value, curses.COLOR_BLACK,
                         curses.COLOR_WHITE)

        self.stdscr = stdscr
        self.height, self.width = self.stdscr.getmaxyx()
        self.menuscr = curses.newwin(int(self.height / 2), self.width, 0, 0)
        self.outscr = curses.newwin(int(self.height / 2), self.width,
                                    int(self.height / 2), 0)

    def add_to_title_q(self, val):
        self.song_name_q.append(val)

    def print_log(self):
        if self.song_name_q:
            text = self.song_name_q.popleft()
            self.menuscr.addstr(self.y, self.x, text)
            self.y += 1
            self.menuscr.refresh()

    def run(self):
        k = 0
        # cursor_y = 0

        # Create menu and out/put windows
        self.outscr.box()

        self.menuscr.box()

        self.outscr.refresh()
        self.menuscr.refresh()

        # Loop where k is the last character pressed
        while k != ord('q'):
            self.print_log()
            # Initialization
            # curses.curs_set(0)

            # cursor_y = max(0, cursor_y)
            # self.print_log()
            # cursor_y = min(len(self.menu) - 1, cursor_y)

            # draw some borders
            #
            #            # refresh screen
            #            printscr.refresh()

            # Wait for next input
            # if k != ord('q'):
            #     k = self.stdscr.getch()
