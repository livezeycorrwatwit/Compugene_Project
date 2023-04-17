
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  exporter.py
#  
#  Copyright 2023 vidali <>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from tkinter import *
from tkinter.filedialog import asksaveasfilename

class exporter:
    def export(self,audio_seg):
        filename = asksaveasfilename(filetypes=[("wav file", ".wav"), ("mp3 file",".mp3"), ("aiff file",".aiff")],defaultextension=".wav")
        print(filename)
        audio_seg.export(filename, format="wav")

    def export2(self,audio_seg): #used for playback
        audio_seg.export("modified.wav", format="wav")
