#! /usr/bin/env python3

import curses
import sys
import os
from curses.textpad import Textbox, rectangle


class Main:

    def __init__(self):
        curses.wrapper(self.start_curses)

    def start_curses(self, stdscr):
        curses.noecho()

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()

        stdscr.refresh()

        # Start colors in curses
        curses.start_color()
        # these are for UI
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)

        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_WHITE)
        curses.init_pair(8, curses.COLOR_RED, curses.COLOR_BLUE)

        self.run(stdscr)

    def run(self, stdscr):
        k = 0
        cursor_y = 0

        height, width = stdscr.getmaxyx()

        # Create menu and output windows
        outscr = curses.newwin(int(height / 2), width, int(height / 2), 0)
        outscr.box()

        menuscr = curses.newwin(int(height / 2), width, 0, 0)
        menuscr.box()

        outscr.refresh()
        menuscr.refresh()

        # Loop where k is the last character pressed
        while k != ord('q'):
            # Initialization
            curses.curs_set(0)

            cursor_y = max(0, cursor_y)
            # cursor_y = min(len(self.menu) - 1, cursor_y)

            # draw some borders
#
#            # refresh screen
#            printscr.refresh()

            # Wait for next input
            if k != ord('q'):
                k = stdscr.getch()


if __name__ == '__main__':
    Main()
