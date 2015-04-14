
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
import designwidget as dw


class OutputDisplay(tk.Frame):

    def __init__(self, parent=None, showrepr=False, *args, **kwargs):
        tk.Frame.__init__(self, parent, borderwidth=1, bg=settings.LED_Color_Oln, relief=tk.FLAT, *args, **kwargs)
        self.parent = parent
        self.grid(padx=5, pady=5, sticky='nswe')
        self.leddisp = [None] * settings.MAX_DIGITS
        self.sinfos = [None] * settings.MAX_DIGITS
        self.design_widget = None

        self.frame_top = tk.Frame(self, borderwidth=10, relief='solid')
        self.frame_top.pack()

        self.frame_leds = tk.Frame(self, borderwidth=10, relief='solid')
        self.frame_leds.pack()

        row = 0
        col = 0
        self.button_desginer = tk.Button(self.frame_top, text='Start Character Designer', command=self._on_design)
        self.button_desginer.pack(side='left', fill='both', expand=True)

        col += 4
        self.button_dump = tk.Button(self.frame_top, text='Dump', command=self._on_dump)
        self.button_dump.pack(side='left', fill='both', expand=True)

        col = settings.DIGITS_PER_COL-2
        self.button_scrollup = tk.Button(self.frame_top, text='<---', command=self._on_scrollup)
        self.button_scrollup.pack(side='right', fill='both', expand=True)

        col = settings.DIGITS_PER_COL-1
        self.button_scrolldn = tk.Button(self.frame_top, text='--->', command=self._on_scrolldn)
        self.button_scrolldn.pack(side='right', fill='both', expand=True)

        row += 1
        col = 0
        self.ledpanel = ledpanel.LEDPanel(self.frame_leds, showrepr=False)
        self.ledpanel.pack(side='top', fill='both', expand=True)

    def getpanel(self):
        return self.ledpanel

    def _on_design(self):
        if self.design_widget is None or not self.design_widget.isalive():
            self.parent.design_widget = dw.DesignWidget(self, self.parent)
            logging.debug("Creating DesignWidget {}".format(self.design_widget))
        else:
            logging.debug("DesignWidget already active")

    def _on_dump(self):
        logging.debug("Dump digit hexvals".format())
        logstr = ''
        for i in range(settings.MAX_DIGITS):
            hexval = self.ledpanel.leddisp[i].segs_to_hex()
            logstr += "0x{:04X}, ".format(hexval)
            if (i + 1) % 8 == 0:
                logging.debug("    {} # ".format(logstr))
                logstr = ''
        if not logstr == '':
            logging.debug("    {} # ".format(logstr))
        pass

    def _on_scrollup(self):
        logging.debug("Scroll up")

    def _on_scrolldn(self):
        logging.debug("Scroll down")
