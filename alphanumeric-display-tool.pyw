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
import random
import logging
import settings
import outputdisplay


class MainApplication(tk.Frame):

    def __init__(self, parent=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, bg=settings.APP_Color_Bgd, *args, **kwargs)
        self.parent = parent
        self.parent.title(settings.APP_Main_Title)
        self.display = outputdisplay.OutputDisplay(self, showrepr=False)
        self.pack(side="top", fill="both", expand=True)
        self.scram_digits = []
        self.scram_running = False

        outstr = map(chr, range(0, 128))

        for i, ch in enumerate(outstr):
            if i < settings.MAX_DIGITS:
                self.display.leddisp[i].char_to_segs(ch)

        for digit in range(settings.MAX_DIGITS):
            self.scram_digits.append({'colors': settings.SCRAM_COLORS, 'segments': settings.SCRAM_SEGMENTS})
        self.scrambler_config(digits=self.scram_digits, speed_ms=settings.SCRAM_SPEED_MS)

    def scrambler_config(self, digits, speed_ms):
        if speed_ms < settings.SCRAM_SPEED_MS_MIN:
            speed_ms = settings.SCRAM_SPEED_MS_MIN
        # logging.debug("scrambler segments={} colors={} speed_ms={}".format(segments, colors, speed_ms))
        if not self.scram_running:
            self._scrambler(digits=digits, speed_ms=speed_ms)

    def _scrambler(self, digits, speed_ms):
        scram_continue = False
        for digit, scram in enumerate(digits):
            # logging.debug("_scrambler digit={} segments={} colors={} speed_ms={}".format(digit, scram['segments'], scram['colors'], speed_ms))
            if scram['segments'] or scram['colors']:
                scram_continue = True
                for wid in self.display.leddisp[digit].seg_ids_to_names:
                    if scram['segments']:
                        self.display.leddisp[digit].set_seg_state(wid, True if random.randint(0, 1) else False)
                    if scram['colors']:
                        self.display.leddisp[digit].set_seg_color(wid, '#{:06X}'.format(random.randint(0, 0xFFFFFF)))
        self.scram_running = scram_continue
        if self.scram_running:
            self.parent.after(speed_ms, self._scrambler, digits, speed_ms)


if __name__ == "__main__":
    logging.basicConfig(filename='', level=logging.DEBUG)
    ROOT = tk.Tk()
    x = settings.INITIAL_HOME[0]
    y = settings.INITIAL_HOME[1]
    ROOT.geometry("+%d+%d" % (x, y))
    APP = MainApplication(ROOT)
    APP.mainloop()
