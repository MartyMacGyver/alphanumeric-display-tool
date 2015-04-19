#!/usr/bin/python

#   Copyright (c) 2015 Martin F. Falatic
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""

"""

from __future__ import print_function

try:  # Python2
    import Tkinter as tk
except ImportError:  # Python3
    import tkinter as tk
import logging
import settings
import ledpanel
import boxes


class MainApplication(tk.Frame):

    def __init__(self, parent=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, bg=settings.APP_Color_Bgd, *args, **kwargs)
        self.parent = parent
        self.parent.title(settings.APP_Main_Title)
        self.led_cols = settings.PANEL_COLS
        self.led_rows = settings.PANEL_ROWS
        self.bufferlen = settings.PANEL_BUFFER
        self.design_widget = None
        self.outstr = ''
        self.startindex = 0
        self.aboutpopup = None
        self.inputpopup = None
        self.scram_colors = False
        self.scram_segments = False

        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Quit", command=parent.quit)

        ctrlmenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Control", menu=ctrlmenu)
        ctrlmenu.add_command(label="Input", command=self._on_input)
        ctrlmenu.add_command(label="Test", command=self._on_test)
        ctrlmenu.add_command(label="Dump", command=self._on_dump)
        ctrlmenu.add_command(label="Random Colors", command=self._on_scramble_colors)
        ctrlmenu.add_command(label="Scramble Segments", command=self._on_scramble_segments)

        helpmenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=self._on_about)

        parent.config(menu=menubar)

        self.ledpanel = ledpanel.LEDPanel(self, showrepr=False, bufferlen=self.bufferlen,
                                          cols=self.led_cols, rows=self.led_rows)
        self.ledpanel.pack(side='top')

        self.frame_nav = tk.Frame(self)
        self.button_scrollup = tk.Button(self.frame_nav, text='<---', command=self._on_scrollup)
        self.button_scrollup.pack(side='left')
        self.label_scroll = tk.Label(self.frame_nav, width=16,
                                     text="0x{:03x} / 0x{:03x}".
                                     format(self.startindex, self.bufferlen))
        self.label_scroll.pack(side='left')
        self.button_scrolldn = tk.Button(self.frame_nav, text='--->', command=self._on_scrolldn)
        self.button_scrolldn.pack(side='left')
        self.frame_nav.pack(side='right')

    def runme(self):
        self.ledpanel.update_display(self.outstr, self.startindex)

    def _on_scramble_colors(self):
        self.scram_colors = not self.scram_colors
        self.ledpanel.scramble_colors(self.scram_colors)

    def _on_scramble_segments(self):
        self.scram_segments = not self.scram_segments
        self.ledpanel.scramble_segments(self.scram_segments)

    def _on_about(self):
        if self.aboutpopup is None or not self.aboutpopup.isalive():
            self.aboutpopup = boxes.AboutBox()

    def _on_input(self):
        if self.inputpopup is None or not self.inputpopup.isalive():
            self.inputpopup = boxes.InputBox(text=self.outstr, callback=self._on_input_result)

    def _on_input_result(self, astring):
        logging.debug("Got result: {}".format(astring))
        self.outstr = astring
        self.ledpanel.update_display(self.outstr, self.startindex)

    def _on_test(self):
        logging.debug("Filling with test chars".format())
        self.outstr = ''.join([chr(x) for x in range(0, 256)])
        self.ledpanel.update_display(self.outstr, self.startindex)

    def _on_dump(self):
        logging.debug("Dump digit hexvals".format())
        logstr = ''
        for i, hexval in enumerate(self.ledpanel.digitdefs['charmap']):
            logstr += "0x{:04X}, ".format(hexval)
            if (i + 1) % 8 == 0:
                logging.debug("    {} # ".format(logstr))
                logstr = ''
        if not logstr == '':
            logging.debug("    {} # ".format(logstr))

    def _on_scrollup(self):
        oldindex = self.startindex
        self.startindex -= self.led_cols
        if self.startindex < 0:
            self.startindex = 0
        if not self.startindex == oldindex:
            self.ledpanel.update_display(self.outstr, self.startindex)
            self.label_scroll.config(text="0x{:03x} / 0x{:03x}".format(self.startindex, self.bufferlen))
        logging.debug("Scroll up: start = {}".format(self.startindex))

    def _on_scrolldn(self):
        oldindex = self.startindex
        self.startindex += self.led_cols
        if self.startindex > self.bufferlen - self.led_rows * self.led_cols:
            self.startindex -= self.led_cols
        if not self.startindex == oldindex:
            self.ledpanel.update_display(self.outstr, self.startindex)
            self.label_scroll.config(text="0x{:03x} / 0x{:03x}".format(self.startindex, self.bufferlen))
        logging.debug("Scroll down: start = {}".format(self.startindex))

if __name__ == "__main__":
    logging.basicConfig(filename='', level=logging.DEBUG)
    ROOT = tk.Tk()
    x = settings.INITIAL_HOME[0]
    y = settings.INITIAL_HOME[1]
    ROOT.geometry("+%d+%d" % (x, y))
    APP = MainApplication(ROOT)
    APP.pack(side='top', fill='both', expand=True)
    APP.runme()
    APP.mainloop()
