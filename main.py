#! /usr/bin/env python3

import curses
import sys
import os
from curses.textpad import Textbox, rectangle


class Main(object):

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
        outscr = curses.newwin(int(height / 8 * 3), width, 0, 0)
        outscr.box()
        menuscr = curses.newwin(int(height / 4), width, int(height / 4 * 3), 0)
        messagescr = curses.newwin(int(5 * height / 8 - height / 4 + 1), width,
                                   int(height / 8 * 3), 0)
        messagescr.box()
        inputscr = curses.newwin(1, width - 2, int(height / 4 * 3) - 2, 1)
        textoutscr = curses.newwin(
            int(5 * height / 8 - height / 4 + 1) - 4, width - 4,
            int(height / 8 * 3) + 1, 2)
        ho, wo = outscr.getmaxyx()
        printscr = curses.newwin(ho - 2, wo - 2, 1, 1)

        stdscr.clear()
        stdscr.refresh()
        outscr.refresh()
        messagescr.refresh()
        textoutscr.refresh()
        inputscr.refresh()

        # Loop where k is the last character pressed
        while k != ord('q'):
            # Initialization
            curses.curs_set(0)

            # key moves
            if k == curses.KEY_DOWN or k == ord('j'):
                cursor_y = cursor_y + 1
            elif k == curses.KEY_UP or k == ord('k'):
                cursor_y = cursor_y - 1
            elif k == curses.KEY_ENTER or k == 10 or k == 13:
                pass

            cursor_y = max(0, cursor_y)
            # cursor_y = min(len(self.menu) - 1, cursor_y)

            # draw some borders
            menuscr.box()

            # refresh screen
            menuscr.refresh()
            printscr.refresh()

            # Wait for next input
            if k != ord('q'):
                k = stdscr.getch()


if __name__ == '__main__':
    Main()
