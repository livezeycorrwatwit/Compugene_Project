
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  deleteAudio.py
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
import os
from tkinter import *

#change the files it deletes
#will need additional functionality later to interact with GUI to change Play/Stop -> Record
def delete(): 

    #button["text"]="RECORD"
    os.remove(os.path.join(__file__[0:__file__.rfind('\\')],"output.wav"))
    os.remove(os.path.join(__file__[0:__file__.rfind('\\')],"decimated.wav"))
    return 0

