"""
EAGLE format BGA plotter

Created on: Feb 19, 2011
Author: Tennessee Carmel-Veilleux (tcv -at- ro.boto.ca)
Revision: $Rev$

Copyright 2011 Tennessee Carmel-Veilleux

Description: 
EAGLE format BGA plotter

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

class EagleBgaPlotter(BgaPlotter):
    def __init__(self, ballList, localValues):
        """
        EAGLE BGA Plotter Implementation.
        
        This version has been tested with EAGLE 4.16r2 and EAGLE 5.11.
        
        Supports all features: courtyard, silkscreen items, footprint pads.
        
        The output script is human-readable. Layers and line widths are
        only changed when necessary, thus reducing file size and improving
        readability.
        """
        BgaPlotter.__init__(self, ballList, localValues)
        self.eagleScriptLines = []
        self.currentLayerId = 1
        self.currentLineWidth = 0.2
        self.layerEquivalents = {"top" : 1, "silkscreen" : 21, "courtyard" : 39}
        
    def draw_pad(self, name, centerPoint, diameter):
        x, y = centerPoint

        self._change_layer("top")

        self._emit_command("SMD %.3f %.3f -100 '%s' (%.3f %.3f);" % (diameter, diameter, name, x, y))
    
    def draw_line(self, name, startPoint, endPoint, lineWidth, layer):
        x1, y1 = startPoint
        x2, y2 = endPoint
        
        self._change_layer(layer)
        self._change_line_width(lineWidth)

        self._emit_command("WIRE '%s' (%.3f %.3f) (%.3f %.3f);" % (name, x1, y1, x2, y2))

    def draw_circle(self, name, centerPoint, diameter, lineWidth, layer):
        x, y = centerPoint
        radius = diameter / 2.0
        
        self._change_layer(layer)
        self._change_line_width(lineWidth)
        
        self._emit_command("CIRCLE (%.3f %.3f) (%.3f %.3f);" % (x, y, x + radius, y))
            
    def init_plotter(self):
        # Initialize EAGLE script with correct drawing options
        self._emit_command("CHANGE style continuous;")
        self._emit_command("GRID mm;")
        self._emit_command("SET wire_bend 2;")
        self._emit_command("CHANGE layer %d;" % self.currentLayerId)
        self._emit_command("CHANGE width %.3f;" % self.currentLineWidth)
    
    def finish_plotter(self):
        # Terminate EAGLE script
        self._emit_command("GRID last;")
        
        # Output EAGLE script
        resultString = "\n".join(self.eagleScriptLines)
        return resultString

    def _change_layer(self, layerName):
        if layerName not in self.layerEquivalents:
            # Catch wrong layer names
            raise RuntimeError("Layer %s not valid for EAGLE !" % layerName)
        else:
            # Emit a layer change command only if necessary
            layerId = self.layerEquivalents[layerName]
            if layerId != self.currentLayerId:
                self._emit_command("CHANGE layer %d;" % layerId)
                self.currentLayerId = layerId

    def _change_line_width(self, lineWidth):
        # Emit a line width change command only if necessary
        if lineWidth != self.currentLineWidth:
            self._emit_command("CHANGE width %.3f;" % lineWidth)
            self.currentLineWidth = lineWidth
                
    def _emit_command(self, command):
        """
        Emit an EAGLE "command" string to the output script.
        """
        self.eagleScriptLines.append(command)
