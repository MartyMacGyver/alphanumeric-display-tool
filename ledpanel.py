
#   Copyright (c) 2015-2020 Martin F. Falatic
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
        self.chrbuffer = ' ' * self.disp_digits
        self.startidx = 0
        self.leddisp = [None] * self.disp_digits
        self.sinfos = [None] * self.disp_digits
        self.scram_digits = [None] * self.disp_digits
        self.design_widget = None
        self.scram_running = False
        self.digitdefs = copy.deepcopy(config_alpha16dp.DIGIT_ALPHA_16_DP)

        logging.debug("Set up panel".format())
        row = 0
        col = 0
        for digit in range(self.disp_digits):
            reprbox = None
            if showrepr:
                reprbox = tk.Entry(self, width=6, bd=2, font='Courier 6 normal', justify='center',
                                   bg='gray25', fg='yellow',
                                   disabledbackground='lightgray', disabledforeground='yellow',
                                   highlightbackground='black', highlightcolor='red', highlightthickness=1)
                self.sinfos[digit] = reprbox
            self.leddisp[digit] = leddigit.LEDdigit(self, digit=digit, reprbox=reprbox, digitdefs=self.digitdefs,
                                                    outline=settings.LED_Color_Oln, activefill=None,
                                                    clickable=True)
            self.leddisp[digit].grid(row=row + 0, column=col, padx=0, pady=0, columnspan=1)
            self.scram_digits[digit] = {'colors': False, 'segments': False}
            if showrepr:
                self.sinfos[digit].grid(row=row + 1, column=col, padx=0, pady=0, sticky='nswe', columnspan=1)
            col += 1
            if (col) % settings.PANEL_COLS == 0:
                row += 1
                if showrepr:
                    row += 1
                col = 0
        self.scramble_colors(False)

    def update_display(self, chrbuffer='', start=0):
        self.chrbuffer = chrbuffer + str(' ' * self.bufferlen)
        self.startidx = start
        self.refresh()

    def refresh(self):
        for digit, ch in enumerate(self.chrbuffer[self.startidx:]):
            if digit < self.disp_digits:
                self.leddisp[digit].char_to_segs(ch)

    def scramble_colors(self, isactive=True):
        for digit in range(self.disp_digits):
            self.scram_digits[digit]['colors'] = isactive
        self.scrambler_config(digits=self.scram_digits, speed_ms=settings.SCRAM_SPEED_MS)

    def scramble_segments(self, isactive=True):
        for digit in range(self.disp_digits):
            self.scram_digits[digit]['segments'] = isactive
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
            if scram['segments'] or scram['colors']:
                scram_continue = True
            ch = '\0x00'
            if len(self.chrbuffer[self.startidx:]) >= digit:
                ch = self.chrbuffer[self.startidx:][digit]
            # logging.debug("_scrambler digit={} ord={} segments={} colors={} speed_ms={}".
            #     format(digit, ord(ch), scram['segments'], scram['colors'], speed_ms))
            for seg_name in self.leddisp[digit].seg_ids_to_names:
                if scram['segments']:
                    self.leddisp[digit].set_seg_state(seg_name, True if random.randint(0, 1) else False)
                else:
                    self.leddisp[digit].set_seg_state(seg_name, self.leddisp[digit].mapped_seg_state(seg_name, ord(ch)))
                if scram['colors']:
                    self.leddisp[digit].set_seg_color(seg_name, '#{:06X}'.format(random.randint(0, 0xFFFFFF)))
                else:
                    self.leddisp[digit].set_seg_color(seg_name)
        self.scram_running = scram_continue
        if self.scram_running:
            self.parent.after(speed_ms, self._scrambler, digits, speed_ms)
