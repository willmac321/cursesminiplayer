#!/usr/bin/env python3
import curses
import enum
from collections import deque
import player.buttons_constants as buttons
# from curses.textpad import Textbox, rectangle


class Color(enum.Enum):
    background = 1
    text = 2
    status_bar = 3
    buttons = 4


class Curse:

    def __init__(self):
        stdscr = curses.initscr()

        # Start colors in curses
        curses.start_color()

        # curses start up settings
        curses.noecho()
        # curses.cbreak()
        t, o = curses.mousemask(curses.ALL_MOUSE_EVENTS |
                                curses.REPORT_MOUSE_POSITION)
        stdscr.keypad(True)
        curses.curs_set(0)
        # print("\033[?1003h\n")
        stdscr.nodelay(True)

        self.song_info_q = deque()
        self.info = None
        self.y_title = 1
        self.x_title = 1
        self.y_artist = 3
        self.x_artist = 1
        self.y_album = 4
        self.x_album = 1

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()

        stdscr.refresh()

        self.set_colors()

        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()  # 12, 60
        self.allscr = curses.newwin(self.height, self.width, 0, 0)

        # setup play status bar
        self.status_bar_window = curses.newwin(3, self.width - 2,
                                               self.height - 4, 1)

        # the music info screen
        self.infoscr = curses.newwin(5, int(self.width / 2), self.height - 13,
                                     int(self.width / 4))

        self.button_right, self.button_left, self.button_play =\
            self.create_buttons(self.height - 7, self.width)

        self.log_scr = curses.newwin(10, self.width - 2, 1, 1)

    def set_colors(self):
        # these are for UI
        curses.init_pair(Color.background.value, curses.COLOR_CYAN,
                         curses.COLOR_BLACK)
        curses.init_pair(Color.text.value, curses.COLOR_BLACK,
                         curses.COLOR_WHITE)
        curses.init_pair(Color.status_bar.value, curses.COLOR_BLUE,
                         curses.COLOR_MAGENTA)
        curses.init_pair(Color.buttons.value, curses.COLOR_CYAN,
                         curses.COLOR_BLACK)

    def mouse_click(self, x, y):
        if self.button_right.enclose(y, x):
            self.draw_button(self.button_right, buttons.RIGHT_ARROW_OUTLINE,
                             Color.background.value)
            self.button_right.refresh()
            return 'next'
        elif self.button_left.enclose(y, x):
            return 'prev'
        elif self.button_play.enclose(y, x):
            return 'play'
        elif self.status_bar_window.enclose(y, x):
            return x
        return 'nahthing'

    def create_buttons(self, height, width):
        # the buttons
        left = self.allscr.derwin(3, 4, height, int(1 * width / 4) - 5)
        play = self.allscr.derwin(3, 5, height, int(width / 2) - 2)
        right = self.allscr.derwin(3, 4, height, int(3 * width / 4) + 1)

        return right, left, play

    def draw_buttons(self):
        self.draw_button(self.button_right, buttons.RIGHT_ARROW_OUTLINE)
        self.draw_button(self.button_left, buttons.LEFT_ARROW_OUTLINE)
        self.draw_button(self.button_play, buttons.PAUSE_OUTLINE)

        self.button_right.border()

        self.button_right.refresh()
        self.button_left.refresh()
        self.button_play.refresh()

    def draw_button(self,
                    window,
                    const,
                    color=Color.buttons.value,
                    offset_x=0,
                    offset_y=0):
        c = 0
        for v in const.split('\n'):
            window.addstr(c + offset_y, offset_x, v,
                          curses.color_pair(color) | curses.A_BOLD)
            c += 1
        return window

    def update_status_bar(self, percent):
        #  self.infoscr.addstr(self.y_title + 1, self.x_title, str(percent))
        #  self.infoscr.refresh()

        y, x = self.status_bar_window.getmaxyx()
        x -= 2

        percent = percent if percent <= 1 else 1
        self.status_bar_window.hline(1, 1, ' ', int(percent * x),
                                     curses.color_pair(Color.status_bar.value))
        self.status_bar_window.refresh()

    def clear_status_bar(self):
        y, x = self.status_bar_window.getmaxyx()
        x -= 2
        self.status_bar_window.hline(1, 1, ' ', int(x))

    def add_to_info_q(self, val):
        self.song_info_q.append(val)

    def print_info(self):
        if self.song_info_q:
            # clear everything
            self.clear_status_bar()
            self.clear_info()
            self.info = self.song_info_q.popleft()
            self.print_title()
            self.print_artists()
            self.print_album()
            self.infoscr.refresh()

    def clear_info(self):
        y, x = self.infoscr.getmaxyx()
        x -= 2
        self.infoscr.hline(self.y_title, self.x_title, ' ', int(x))
        self.infoscr.hline(self.y_artist, self.x_artist, ' ', int(x) * 2)
        self.infoscr.hline(self.y_album, self.x_album, ' ', int(x) * 2)

    def print_title(self):
        y, x = self.infoscr.getmaxyx()
        name = self.info['name']
        if len(name) > (x - 2):
            name = name[0:(x - 2) - 3] + '...'

        self.infoscr.addstr(self.y_title, self.x_title, name,
                            curses.A_BOLD)

    def print_album(self):
        y, x = self.infoscr.getmaxyx()
        name = self.info['album']['name']
        if len(name) > (x - 2):
            name = name[0:(x - 2) - 3] + '...'
        self.infoscr.addstr(self.y_album, self.x_album,
                            name, curses.A_DIM)

    def print_artists(self):
        artists = ''
        length = 0
        y, x = self.infoscr.getmaxyx()
        for a in self.info['artists']:
            if length == 0:
                artists = a['name']
                length += 1
            else:
                artists = artists + ', ' + a['name']

        self.debug(artists)
        if len(artists) > (x - 2):
            artists_out = artists[0:(x - 2) - 3] + '...'
        else:
            artists_out = artists

        self.infoscr.addstr(self.y_artist, self.x_artist, artists_out)

    def draw_boxes(self):
        # cursor_y = 0

        self.allscr.box()
        self.allscr.refresh()

        self.draw_buttons()

        self.status_bar_window.border()
        self.status_bar_window.refresh()

        # self.infoscr.box()
        # self.infoscr.refresh()

    def debug(self, message):
        self.log_scr.addstr(str(message) + ' ')
        self.log_scr.refresh()

    def kill(self):
        self.stdscr.nodelay(False)
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
