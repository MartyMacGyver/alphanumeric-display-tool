
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


class DesignWidget(tk.Frame):

    IEXIST = False

    def __init__(self, parent=None, *args, **kwargs):
        if not self.IEXIST:
            tk.Frame.__init__(self, parent, borderwidth=1, bg=settings.LED_Color_Oln, relief=tk.FLAT, *args, **kwargs)
            self.IEXIST = True
            self.top = tk.Toplevel(parent)
            self.top.title("Character Designer")
            self.label = tk.Label(self.top, text="Click the segments...")
            self.entry = tk.Entry(self.top)
            self.button_done = tk.Button(self.top, text='Done', command=self._on_done)
            self.sinfo = tk.Entry(self.top, width=6, bd=2, font="Courier 8 normal", justify="center",
                                  bg="gray25", fg="yellow",
                                  disabledbackground="lightgray", disabledforeground="yellow",
                                  highlightbackground="black", highlightcolor="red", highlightthickness=1)
            self.leddisp = leddigit.LEDdigit(self.top, digit=0, scale=(2, 2), reprbox=self.sinfo, clickable=True,
                                             outline=settings.LED_Color_Oln, activefill=settings.LED_Color_Sel)
            self.label.pack()
            self.leddisp.pack()
            self.sinfo.pack(expand=1, fill=tk.BOTH)
            self.entry.pack()
            self.button_done.pack()

    def _on_done(self):
        self.value = self.entry.get()
        self.IEXIST = False
        self.top.destroy()

    def isalive(self):
        logging.debug("Popup")
        return self.IEXIST
