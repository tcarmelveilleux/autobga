"""
XML format BGA plotter

Created on: Feb 7, 2011
Author: Tennessee Carmel-Veilleux (tcv -at- ro.boto.ca)
Revision: $Rev$

Copyright 2011 Tennessee Carmel-Veilleux

Description: 
XML format BGA plotter

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
import datetime

class XMLBgaPlotter(BgaPlotter):
    def __init__(self, ballList, localValues, version):
        """
        XML BGA Plotter Implementation.
        
        Supports all features: courtyard, silkscreen items, footprint pads.
        TODO: Mention where to find XML Schema
        """
        BgaPlotter.__init__(self, ballList, localValues)
        self.localValues = localValues
        self.xmlList = []
        self.version = version
        
        self.layerEquivalents = {"top" : "topLayer", "silkscreen" : "topSilkScreen", "courtyard" : "topCourtyard"}
        
    def draw_pad(self, name, centerPoint, diameter):
        x, y = centerPoint
        
        self.xmlList.append('<padElement name="%s" layer="topLayer" thickness="0" xPos="%.3f" yPos="%.3f" width="%.3f" height="%.3f" angle="0" padShape="circle" maxTextHeight="%.3f"/>' % (name, x, y, diameter, diameter, 0.8*diameter))
    
    def draw_line(self, name, startPoint, endPoint, lineWidth, layer):
        x1, y1 = startPoint
        x2, y2 = endPoint
        
        if layer not in self.layerEquivalents:
            # Catch wrong layer names
            raise RuntimeError("Layer %s not valid for XML !" % layer)
        
        self.xmlList.append('<lineElement name="%s" layer="%s" thickness="%.3f" x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f"/>' % \
                            (name, self.layerEquivalents[layer], lineWidth, x1, y1, x2, y2))

    def draw_circle(self, name, centerPoint, diameter, lineWidth, layer):
        x, y = centerPoint
        
        if layer not in self.layerEquivalents:
            # Catch wrong layer names
            raise RuntimeError("Layer %s not valid for XML !" % layer)
                
        self.xmlList.append('<circleElement name="%s" layer="%s" thickness="%.3f" xPos="%.3f" yPos="%.3f" diameter="%.3f"/>' % \
                            (name, self.layerEquivalents[layer], lineWidth, x, y, diameter))
        
    def init_plotter(self):
        # Emit file header with package description.
        currentDate = datetime.datetime.utcnow()
        self.localValues["date"] = currentDate.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.localValues["version"] = self.version
        self.xmlList.append("""<?xml version="1.0" encoding="UTF-8"?>
<footprintLibrary xmlns="http://www.tentech.ca/schemas/FootprintLibrary"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" generator = "AutoBGA"
 version="%(version)s" exportDate="%(date)s">
    <description>Single footprint generated with AutoBGA</description>
    <footprints>
        <footprint name="bga_%(width)d_%(height)d">
            <description>BGA %(width)d x %(height)d balls, %(pitch).3f mm pitch, %(packageWidth).3f mm(width) x %(packageHeight).3f mm(height) body size</description>
            <geometry>
            """ % self.localValues)
    
    def finish_plotter(self):
        # Emit file footer to correctly finish the tree
        self.xmlList.append("""
            </geometry>
        </footprint>
    </footprints>
</footprintLibrary>""")
                
        # Output XML tree
        resultString = "\n".join(self.xmlList)
        return resultString
