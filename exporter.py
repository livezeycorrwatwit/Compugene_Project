
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

import os
import pyaudio #fix in install script
import wave

class exporter:
	def export(audio_seg, filename):
		audio_seg.export(filename, format="wav")

#merge the two of these together
def export():
    newfile = asksaveasfilename(filetypes=[("wav file", ".wav")],defaultextension=".wav")
                
    reader=wave.open("newfile.wav",'rb')
    a1 = reader.getnchannels()
    a2 = reader.readframes(reader.getnframes())
    reader.close()

    writer=wave.open(newfile,'wb')
    writer.setnchannels(reader.getnchannels())
    writer.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
    writer.setframerate(int(44100))
    writer.writeframes(a2)

    writer.close()
    pyaudio.PyAudio().terminate()
                