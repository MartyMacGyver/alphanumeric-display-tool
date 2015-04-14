
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


class InputBox(tk.Frame):

    IEXIST = False

    def __init__(self, parent=None, text='', callback=None, *args, **kwargs):
        if not self.IEXIST:
            tk.Frame.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            self.callback = callback
            self.IEXIST = True
            self.top = tk.Toplevel(self)
            self.astring = text

            self.top.title("Entry")
            self.top.protocol("WM_DELETE_WINDOW", self._closeme)
            self.label = tk.Label(self.top, text="Enter text to display")
            self.label.pack()
            self.entry = tk.Entry(self.top, width=80)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.astring)
            self.entry.pack()
            self.button_ok = tk.Button(self.top, text='OK', command=self._on_ok)
            self.button_ok.pack()
            self.button_cancel = tk.Button(self.top, text='Cancel', command=self._on_cancel)
            self.button_cancel.pack()
            self.top.wait_visibility()
            self.top.grab_set()

            self.astring = ''

    def _on_ok(self):
        self.astring = self.entry.get()
        if self.callback is not None:
            self.callback(self.astring)
        self._closeme()

    def _on_cancel(self):
        self._closeme()

    def _closeme(self):
        self.IEXIST = False
        self.top.grab_release()
        self.top.destroy()

    def isalive(self):
        logging.debug("InputBox is {}".format(self.IEXIST))
        return self.IEXIST


class AboutBox(tk.Frame):

    IEXIST = False

    def __init__(self, parent=None, callback=None, *args, **kwargs):
        if not self.IEXIST:
            tk.Frame.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            self.callback = callback
            self.IEXIST = True
            self.top = tk.Toplevel(self)

            self.top.title("About")
            self.top.protocol("WM_DELETE_WINDOW", self._on_ok)
            self.label = tk.Label(self.top, text=settings.APP_Main_Title)
            self.label.pack()
            self.button_ok = tk.Button(self.top, text='OK', command=self._on_ok)
            self.button_ok.pack()
            self.top.wait_visibility()
            self.top.grab_set()

    def _on_ok(self):
        if self.callback is not None:
            self.callback()
        self._closeme()

    def _closeme(self):
        self.IEXIST = False
        self.top.grab_release()
        self.top.destroy()

    def isalive(self):
        logging.debug("AboutBox is {}".format(self.IEXIST))
        return self.IEXIST
