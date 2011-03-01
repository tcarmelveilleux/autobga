"""
TSV (tab-separated values) format BGA plotter

Created on: Feb 19, 2011
Author: Tennessee Carmel-Veilleux (tcv -at- ro.boto.ca)
Revision: $Rev$

Copyright 2011 Tennessee Carmel-Veilleux

Description: 
TSV (tab-separated values) format BGA plotter

License:
Copyright (c) 2011, Tennessee Carmel-Veilleux
All rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are 
met:

    * Redistributions of source code must retain the above copyright 
notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above 
copyright notice, this list of conditions and the following disclaimer 
in the documentation and/or other materials provided with the 
distribution.
    * Neither the name of SONIA AUV nor the names of its contributors 
may be used to endorse or promote products derived from this software 
without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR 
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT 
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from BgaPlotter import *

class TSVBgaPlotter(BgaPlotter):
    def __init__(self, ballList, localValues):
        """
        TSV BGA Plotter implementation.
        
        Simply output a list of pads present with their pad name,
        position and diameter.
        
        No silkscreen item or courtyard are included.
        """
        BgaPlotter.__init__(self, ballList, localValues)
        self.tsvList = []
                
    def draw_pad(self, name, centerPoint, diameter):
        x, y = centerPoint
        self.tsvList.append("%s\t%.3f\t%.3f\t%.3f" % (name, x, y, diameter))
    
    def draw_line(self, name, startPoint, endPoint, lineWidth, layer):
        # Lines are omitted from TSV
        pass
    
    def draw_circle(self, name, centerPoint, diameter, lineWidth, layer):
        # Circles are omitted from TSV
        pass
            
    def init_plotter(self):
        # Write TSV file header
        self.tsvList.append("Pad name\tX position (mm)\tY position (mm)\tPad diameter (mm)")
    
    def finish_plotter(self):        
        # Output TSV file text
        resultString = "\n".join(self.tsvList)        
        return resultString
