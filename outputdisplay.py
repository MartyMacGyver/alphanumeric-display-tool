
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
import leddigit
import designwidget as dw


class OutputDisplay(tk.Frame):

    def __init__(self, parent=None, showrepr=False, *args, **kwargs):
        tk.Frame.__init__(self, parent, borderwidth=1, bg=settings.LED_Color_Oln, relief=tk.FLAT, *args, **kwargs)
        self.parent = parent
        self.grid(padx=10, pady=10, sticky='nswe')
        self.leddisp = [None] * settings.MAX_DIGITS
        self.sinfos = [None] * settings.MAX_DIGITS
        self.design_widget = None
        row = 0
        col = 0
        self.button_desginer = tk.Button(self, text='Start Character Designer', command=self._on_design)
        self.button_desginer.grid(row=row, column=col, padx=10, pady=10, sticky='nw', columnspan=4)
        col += 4
        self.button_dump = tk.Button(self, text='Dump', command=self._on_dump)
        self.button_dump.grid(row=row, column=col, padx=10, pady=10, sticky='nw', columnspan=1)
        col = settings.DIGITS_PER_COL-2
        self.button_dump = tk.Button(self, text='<---', command=self._on_scrollup)
        self.button_dump.grid(row=row, column=col, padx=10, pady=10, sticky='nw', columnspan=1)
        col = settings.DIGITS_PER_COL-1
        self.button_dump = tk.Button(self, text='--->', command=self._on_scrolldn)
        self.button_dump.grid(row=row, column=col, padx=10, pady=10, sticky='nw', columnspan=1)
        row += 1
        col = 0
        for i in range(settings.MAX_DIGITS):
            reprbox = None
            if showrepr:
                reprbox = tk.Entry(self, width=6, bd=2, font="Courier 6 normal", justify="center",
                                   bg="gray25", fg="yellow",
                                   disabledbackground="lightgray", disabledforeground="yellow",
                                   highlightbackground="black", highlightcolor="red", highlightthickness=1)
                self.sinfos[i] = reprbox
            self.leddisp[i] = leddigit.LEDdigit(self, digit=i, reprbox=reprbox,
                                                outline=settings.LED_Color_Oln, activefill=None,
                                                clickable=True)
            self.leddisp[i].grid(row=row + 0, column=col, padx=0, pady=0, columnspan=1)
            if showrepr:
                self.sinfos[i].grid(row=row + 1, column=col, padx=0, pady=0, sticky='nswe', columnspan=1)
            col += 1
            if (col) % settings.DIGITS_PER_COL == 0:
                row += 1
                if showrepr:
                    row += 1
                col = 0

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
            hexval = self.leddisp[i].segs_to_hex()
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
