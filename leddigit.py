
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
from collections import OrderedDict
import logging
import settings


class LEDdigit(tk.Canvas):

    def __init__(self, parent=None, reprbox=None, digit=None, clickable=False,
                 outline=None, activefill=None, digitdefs=None,
                 scale=settings.LED_Scale, pad_nswe=settings.LED_Pad):
        tk.Canvas.__init__(self, parent, borderwidth=0, relief=tk.FLAT, highlightthickness=0)
        self.parent = parent
        self.clickable = clickable
        self.reprbox = reprbox
        self.digit = digit
        self.curcharidx = ord(' ')
        self.digitdefs = digitdefs
        self.pad_nswe = pad_nswe
        self.is_pressed = False
        self.seg_states = OrderedDict()
        self.seg_ids_to_names = OrderedDict()
        self.seg_names_to_ids = OrderedDict()
        self.ledcoloron = settings.LED_Color_On
        self.scram_running = False
        self.scram_colors = False
        self.scram_segments = False

        logging.debug("Set up digit {}".format(self.digit))
        for seg_name in self.digitdefs['polygons']:
            points = []
            xsum = 0.0
            ysum = 0.0
            for t in self.digitdefs['polygons'][seg_name]['pts']:
                x = t[0] * scale[0] + self.pad_nswe[0]
                xsum += x
                y = t[1] * scale[1] + self.pad_nswe[2]
                ysum += y
                points.append((x, y))
            npts = len(self.digitdefs['polygons'][seg_name]['pts'])
            centroid = (int(xsum / npts), int(ysum / npts))
            self.seg_states[seg_name] = False
            fill = self.ledcoloron if self.seg_states[seg_name] else settings.LED_Color_Off
            seg_id = self.create_polygon(points, outline=outline, fill=fill, activefill=activefill,
                                         width=1, activewidth=1)
            self.seg_ids_to_names[seg_name] = seg_id
            self.seg_names_to_ids[seg_id] = seg_name
            if self.clickable:
                self.tag_bind(seg_id, '<ButtonPress-1>', self._on_press)
                self.tag_bind(seg_id, '<ButtonRelease-1>', self._on_release)
                # self.tag_bind(seg_id, '<Enter>', self._on_enter)
                # self.tag_bind(seg_id, '<Leave>', self._on_leave)
            else:
                self.create_oval(centroid[0] - 1 * scale[0], centroid[1] - 1 * scale[1],
                                 centroid[0] + 1 * scale[0], centroid[1] + 1 * scale[1],
                                 outline=outline)
            logging.debug("  - Segment {} centroid = {}".format(seg_name, centroid))
        logging.debug("  - {}  {}".format(self.seg_ids_to_names, self.seg_names_to_ids))
        self.reprbox_update()
        (x0, y0, x1, y1) = self.bbox('all')
        logging.debug("  - bbox = ({},{},{},{})".format(x0, y0, x1, y1))
        height = (y1) + self.pad_nswe[1]
        width = (x1) + self.pad_nswe[3]
        self.configure(width=width, height=height, bg=settings.LED_Color_Bgd)

    def char_to_segs(self, ch):
        self.curcharidx = ord(ch)
        for seg_name in self.digitdefs['bitmap']:
            self.set_seg_state(seg_name, self.mapped_seg_state(seg_name, self.curcharidx))
            self.set_seg_color(seg_name)
        # logging.debug("{:d} 0x{:04X}".format(self.curcharidx, self.digitdefs['charmap'][self.curcharidx]))

    def mapped_seg_state(self, seg_name, chidx):
        mask = 1 << (self.digitdefs['bitmap'][seg_name]['block'] * 4 + self.digitdefs['bitmap'][seg_name]['bit'])
        return True if self.digitdefs['charmap'][chidx] & mask else False

    def reprbox_update(self):
        repstr = self.segs_to_repr_hex()
        if self.reprbox is not None:
            self.reprbox.delete(0, tk.END)
            self.reprbox.insert(0, repstr)

    def segs_to_repr_bin(self):
        repstr = ''
        for seg_name in self.digitdefs['repr']:
            if seg_name == '':
                repstr += ' '  # '-'
            else:
                repstr += '1' if self.seg_states[seg_name] else '0'
        return repstr

    def segs_to_repr_hex(self):
        repstr = "0x{:04X}".format(self.segs_to_hex())
        return repstr

    def segs_to_hex(self):
        hexval = 0x0
        mask = 0x1
        for seg_name in self.digitdefs['bitmap']:
            if not seg_name == '':
                mask = 1 << (self.digitdefs['bitmap'][seg_name]['block'] * 4 + self.digitdefs['bitmap'][seg_name]['bit'])
                hexval += mask if self.seg_states[seg_name] else 0
                mask <<= 1
        return hexval

    def set_seg_color(self, name, color=None):
        if color is None:
            color = self.ledcoloron
        fill = color if self.seg_states[name] else settings.LED_Color_Off
        self.itemconfigure(self.seg_ids_to_names[name], fill=fill)

    def set_seg_state(self, name, state=None):
        if state is not None:
            self.seg_states[name] = state
        self.reprbox_update()

    def _on_press(self, event):
        seg_id = event.widget.find_withtag('current')[0]
        self.is_pressed = True
        if seg_id in self.seg_names_to_ids:
            x = self.winfo_pointerx()
            y = self.winfo_pointery()
            seg_name = self.seg_names_to_ids[seg_id]
            event_str = "{} {} {} {}".format(seg_id, seg_name, x, y)
            logging.debug("_on_press {}".format(event_str))

    def _on_release(self, event):
        seg_id = event.widget.find_withtag('current')[0]
        if seg_id in self.seg_names_to_ids and self.is_pressed:
            x = self.winfo_pointerx()
            y = self.winfo_pointery()
            seg_name = self.seg_names_to_ids[seg_id]
            self.seg_states[seg_name] = not self.seg_states[seg_name]
            fill = self.ledcoloron if self.seg_states[seg_name] else settings.LED_Color_Off
            self.itemconfigure(seg_id, fill=fill)
            self.reprbox_update()
            self.digitdefs['charmap'][self.curcharidx] = self.segs_to_hex()
            event_str = "{} {} {} {}".format(seg_id, seg_name, x, y)
            logging.debug("_on_release {}".format(event_str))
            self.parent.refresh()
        self.is_pressed = False

    def _on_enter(self, event):
        seg_id = event.widget.find_withtag('current')[0]
        if seg_id in self.seg_names_to_ids:
            x = self.winfo_pointerx()
            y = self.winfo_pointery()
            seg_name = self.seg_names_to_ids[seg_id]
            event_str = "{} {} {} {}".format(seg_id, seg_name, x, y)
            logging.debug("_on_enter {}".format(event_str))

    def _on_leave(self, event):
        seg_id = event.widget.find_withtag('current')[0]
        if seg_id in self.seg_names_to_ids:
            x = self.winfo_pointerx()
            y = self.winfo_pointery()
            seg_name = self.seg_names_to_ids[seg_id]
            event_str = "{} {} {} {}".format(seg_id, seg_name, x, y)
            logging.debug("_on_leave {}".format(event_str))
