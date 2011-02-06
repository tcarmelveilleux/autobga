"""
AutoBGA BGA Pad name generator module

Created on: 7/09/2010
Author: Tennessee Carmel-Veilleux (tcv -at- ro.boto.ca)
Revision: $Rev$

Copyright 2010 Tennessee Carmel-Veilleux

Description: 
BgaPadNameGenerator class that generates a grid of BGA pad names based
on orientation parameters.

License:
Copyright (c) 2010, Tennessee Carmel-Veilleux
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

class BgaPadNameGenerator:
    def __init__(self, width, height, pinA1Corner):
        """
        Initializes a BGA pad name generator for a BGA of
        "width" x "height" and "pinA1Corner" pin A1 position.
        Valid values for "pinA1Corner" are "NW", "NE", "SW", "SE"
        """
        self.width = width
        self.height = height

        # Determine direction of progression
        if pinA1Corner.upper() == "NW":
            self.vDirection = "down"
            self.hDirection = "right"
        elif pinA1Corner.upper() == "NE":
            self.vDirection = "down"
            self.hDirection = "left"
        elif pinA1Corner.upper() == "SE":
            self.vDirection = "up"
            self.hDirection = "left"
        elif pinA1Corner.upper() == "SW":
            self.vDirection = "up"
            self.hDirection = "right"
        else:
            raise ValueError("Unknown corner designator: '%s'" % pinA1Corner)
        
        # Create a 2D grid of strings indexed as [x][y]
        self.grid = [([""] * height) for i in xrange(width)]
        
        # Create a list of valid letters
        self.letters = [letter for letter in "ABCDEFGHJKLMNPRTUVWY"]
        self.nLetters = len(self.letters)
            
    def _getRowName(self, yIdx):
        if yIdx < self.nLetters:
            return self.letters[yIdx]
        else:
            return "%s%s" % (self.letters[(yIdx / self.nLetters) - 1], self.letters[yIdx % self.nLetters])
        
    def generatePadNames(self):
        """
        Returns a 0-indexed 2D grid of size (self.width x self.height)
        with [x][y] indexing as [row][column] containing the pad labels
        associated with each position.
        """
        for yIdx in xrange(self.height):
            rowName = self._getRowName(yIdx)
            for xIdx in xrange(self.width):
                self.grid[xIdx][yIdx] = "%s%d" % (rowName, (xIdx + 1))
        
        if self.hDirection == "left":
            self.grid.reverse()
            
        if self.vDirection == "up":
            for column in xrange(self.width):
                self.grid[column].reverse()
        
        return self.grid
    
    def dump(self):
        """
        Dumps the grid on screen
        """
        for yIdx in xrange(self.height):
            row = ""
            for xIdx in xrange(self.width):
                row += "%4s " % self.grid[xIdx][yIdx]
            print row
        
if __name__ == "__main__":
    gNW = BgaPadNameGenerator(22,22,"NW")
    gNE = BgaPadNameGenerator(22,22,"NE")
    gSW = BgaPadNameGenerator(22,22,"SW")
    gSE = BgaPadNameGenerator(22,22,"SE")
    
    gNW.generatePadNames()
    gNE.generatePadNames()
    gSW.generatePadNames()
    gSE.generatePadNames()
    
    gNW.dump()
    print
    gNE.dump()
    print
    gSW.dump()
    print
    gSE.dump()
    