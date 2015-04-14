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


class MainApplication(tk.Frame):

    def __init__(self, parent=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, bg=settings.APP_Color_Bgd, *args, **kwargs)
        self.parent = parent
        self.parent.title(settings.APP_Main_Title)
        self.parent = parent
        self.led_cols = 16
        self.led_rows = 4
        self.bufferlen = 256
        self.design_widget = None
        self.outstr = ""
        self.startindex=0

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label="Dump", command=self._on_dump)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=parent.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        designmenu = tk.Menu(menubar, tearoff=False)
        menubar.add_command(label="Dump", command=self._on_dump)
        helpmenu = tk.Menu(menubar, tearoff=False)
        menubar.add_command(label="Test", command=self._on_test)
        helpmenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=None)
        parent.config(menu=menubar)

        self.ledpanel = ledpanel.LEDPanel(self, showrepr=False, bufferlen=self.bufferlen,
                                          cols=self.led_cols, rows=self.led_rows)
        self.ledpanel.pack(side='top')

        self.frame_nav = tk.Frame(self)
        self.button_scrollup = tk.Button(self.frame_nav, text='<---', command=self._on_scrollup)
        self.button_scrollup.pack(side='left')
        self.button_scrolldn = tk.Button(self.frame_nav, text='--->', command=self._on_scrolldn)
        self.button_scrolldn.pack(side='left')
        self.frame_nav.pack(side='right')

    def runme(self):
        self.scram_digits = []
        self.scram_running = False
        self.ledpanel.update_display(self.outstr, self.startindex)

    def _on_test(self):
        logging.debug("Filling with test chars".format())
        self.outstr = ''.join([chr(x) for x in range(0,256)])
        self.ledpanel.update_display(self.outstr, 0)

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
        logging.debug("Scroll up: start = {}".format(self.startindex))

    def _on_scrolldn(self):
        oldindex = self.startindex
        self.startindex += self.led_cols
        if self.startindex > self.bufferlen - self.led_rows * self.led_cols:
            self.startindex -= self.led_cols
        if not self.startindex == oldindex:
            self.ledpanel.update_display(self.outstr, self.startindex)
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
