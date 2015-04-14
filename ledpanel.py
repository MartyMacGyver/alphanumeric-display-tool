
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
import copy
import settings
import leddigit
import config_alpha16dp


class LEDPanel(tk.Frame):

    def __init__(self, parent=None, showrepr=False, rows=0, cols=0, bufferlen=0, *args, **kwargs):
        tk.Frame.__init__(self, parent, borderwidth=10, bg=settings.LED_Color_Oln, relief='sunken', *args, **kwargs)
        self.parent = parent
        self.disp_rows = rows
        self.disp_cols = cols
        self.disp_digits = rows * cols
        self.bufferlen = bufferlen
        self.chrbuffer = ''
        self.startidx = 0
        self.leddisp = [None] * self.disp_digits
        self.sinfos = [None] * self.disp_digits
        self.design_widget = None
        self.scram_digits = []
        self.scram_running = False
        self.digitdefs = copy.deepcopy(config_alpha16dp.DIGIT_ALPHA_16_DP)

        row = 0
        col = 0
        for i in range(self.disp_digits):
            reprbox = None
            if showrepr:
                reprbox = tk.Entry(self, width=6, bd=2, font='Courier 6 normal', justify='center',
                                   bg='gray25', fg='yellow',
                                   disabledbackground='lightgray', disabledforeground='yellow',
                                   highlightbackground='black', highlightcolor='red', highlightthickness=1)
                self.sinfos[i] = reprbox
            self.leddisp[i] = leddigit.LEDdigit(self, digit=i, reprbox=reprbox, digitdefs=self.digitdefs,
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

        for digit in range(self.disp_digits):
            self.scram_digits.append({'colors': settings.SCRAM_COLORS, 'segments': settings.SCRAM_SEGMENTS})
        self.scrambler_config(digits=self.scram_digits, speed_ms=settings.SCRAM_SPEED_MS)

    def update_display(self, chrbuffer='', start=0):
        self.chrbuffer = chrbuffer + str(' ' * self.bufferlen)
        self.startidx = start
        self.refresh()

    def refresh(self):
        
        for i, ch in enumerate(self.chrbuffer[self.startidx : ]):
            if i < self.disp_digits:
                self.leddisp[i].char_to_segs(ch)
        
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
                for wid in self.leddisp[digit].seg_ids_to_names:
                    if scram['segments']:
                        self.leddisp[digit].set_seg_state(wid, True if random.randint(0, 1) else False)
                    if scram['colors']:
                        self.leddisp[digit].set_seg_color(wid, '#{:06X}'.format(random.randint(0, 0xFFFFFF)))
        self.scram_running = scram_continue
        if self.scram_running:
            self.parent.after(speed_ms, self._scrambler, digits, speed_ms)
