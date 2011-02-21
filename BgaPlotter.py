"""
Base class for plotting BGA parts on output devices

Created on: Feb 19, 2011
Author: Tennessee Carmel-Veilleux (tcv -at- ro.boto.ca)
Revision: $Rev$

Copyright 2011 Tennessee Carmel-Veilleux

Description: 
Base class for plotting BGA parts on output devices. Uses template
methods implemented by derived classes to provide specific details
about how geometry is to be output in different formats

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
import math

class BgaPlotter:
    def __init__(self, ballList, localValues):
        """
        """
        self.ballList = ballList[:]

        # Save geometry data locally
        self.layers = ("silkscreen", "courtyard")
        self.packageWidth = localValues["packageWidth"]
        self.packageHeight = localValues["packageHeight"]
        self.ballDiameter = localValues["padDiameter"]
        self.pinA1Corner = localValues["pinA1Corner"]
        self.pinA1Point = localValues["pinA1Point"]
        
        # Line width hardcoded value is 0.2mm (8 mil)
        self.lineWidth = 0.2
        
        # Rotate part to have pad A1 at NW corner
        self._rotate_part()
        
    def draw_pad(self, name, centerPoint, diameter):
        raise NotImplementedError()
    
    def draw_line(self, name, startPoint, endPoint, lineWidth, layer):
        raise NotImplementedError()

    def draw_circle(self, name, centerPoint, diameter, lineWidth, layer):
        raise NotImplementedError()

    def init_plotter(self):
        raise NotImplementedError()
    
    def finish_plotter(self):
        raise NotImplementedError()
    
    def process(self):
        """
        Draw the BGA using the template methods of the class.
        
        The BGA is drawn in 4 steps:
        1- Outline rectangle on silkscreen
        2- Alignment dot on silkscreen
        3- Courtyard rectangle
        4- Ball pads
        
        Prior to drawing, self.init_plotter() is called to initialize
        the concrete plotter.
        
        After drawing, this function returns the value from self.finish_plotter()
        to provide data drawn by the concrete plotter.
        
        Returns a plotString containing the plotted data formatted according to 
        the concrete plotter's particular output format.
        
        Throws a RuntimeError if something fishy happens during plotting.
        """
        # Initialize plotter through template method
        self.init_plotter()
    
        # Step 1: Draw outline rectangle on silkscreen
        outlineUpperLeft = (-self.packageWidth / 2.0, self.packageHeight / 2.0)
        outlineLowerRight = (self.packageWidth / 2.0, -self.packageHeight / 2.0)
        self._draw_rectangle_outline("silkOutline", outlineUpperLeft, outlineLowerRight, self.lineWidth, "silkscreen")

        # Step 2: Draw pin A1 dot on silkscreen in NW corner
        a1x, a1y = self.pinA1Point     
        dotCenter = (-((self.packageWidth / 2.0) + (1.5 * self.lineWidth)), a1y)
        
        self.draw_circle("a1cornerDot", dotCenter, self.lineWidth, self.lineWidth, "silkscreen")
        
        # Step 3: Draw courtyard, based on info from Tom Hausherr's blog post about IPC 7351:
        # "PCB Design Perfection Starts in the CAD Library - Part 6" at
        # http://blogs.mentor.com/tom-hausherr/blog/2010/11/18/pcb-design-perfection-starts-in-the-cad-library-part-6/
        # Consulted on February 4th 2011
        #
        # Quote:
        #   There are different Placement Courtyard spacing rules for Grid Array packages based on ball size:
        #   Ball size above 0.50 mm = 2 mm
        #   Ball size between 0.50 mm & 0.25 mm = 1 mm
        #   Ball size below 0.25 mm = 0.5 mm
        
        # Step 3a: Find courtyard dimensions
        if self.ballDiameter > 0.5:
            courtyard = 2.0
        elif self.ballDiameter < 0.25:
            courtyard = 0.5
        else:
            courtyard = 1.0
            
        # Step 3b: Determine courtyard rectangle coordinates and draw courtyard
        ulx, uly = outlineUpperLeft
        lrx, lry = outlineLowerRight
        upperLeft = (ulx - courtyard + (self.lineWidth / 2.0), uly + courtyard - (self.lineWidth / 2.0))
        lowerRight = (lrx + courtyard - (self.lineWidth / 2.0), lry - courtyard + (self.lineWidth / 2.0))
        self._draw_rectangle_outline("courtyard", upperLeft, lowerRight, self.lineWidth, "courtyard")

        # Step 4: draw all ball pads
        for ball in self.ballList:
            # ball[0] = name
            # ball[1] = X
            # ball[2] = y
            # ball[3] = diameter
            name, x, y, diameter = tuple(ball)
            self.draw_pad(name, (x, y), diameter)

        # Step 5: Draw corner line
        # Step 5a: Find intercept of limit line
        minDistFromA1 = (diameter / 2.0) + self.lineWidth
        
        dLineX = a1x + (minDistFromA1 * math.cos(3.0 * math.pi / 4.0))
        dLineY = a1y + (minDistFromA1 * math.sin(3.0 * math.pi / 4.0))
        if dLineX > (-self.packageWidth / 2.0) and dLineY < (self.packageHeight / 2.0):
            # Limit line is within package, we can try to draw a corner line
            limitIntercept = dLineY - dLineX
        else:
            # Limit line is not within package: we can't draw a corner line
            limitIntercept = None
            
        # Step 5b: Find minimum distance from side desired
        minDistFromSide = min([(self.packageHeight / 2.0) - (a1y + (diameter / 2.0)),
                               (a1x - (diameter / 2.0)) - (-self.packageWidth / 2.0)]) / 2.0
        minCornerDist = math.sqrt(2) * minDistFromSide
        
        cLineX = (-self.packageWidth / 2.0) + (minCornerDist * math.cos(-math.pi / 4.0))
        cLineY = (self.packageHeight / 2.0) + (minCornerDist * math.sin(-math.pi / 4.0))
        cornerIntercept = cLineY - cLineX
        
        # Step 5c: Draw actual corner line
        if limitIntercept:
            if cornerIntercept > limitIntercept:
                # Corner intercept higher than limit intercept: use corner intercept
                intercept = cornerIntercept
            else:
                # Corner intercept would overlap array: use limit intercept
                intercept = limitIntercept

            # Use line equation: y = (1*x) + intercept
            leftEdgePoint = (-self.packageWidth / 2.0, (-self.packageWidth / 2.0) + intercept)
            topEdgePoint = ((self.packageHeight / 2.0) - intercept, (self.packageHeight / 2.0))
            
            self.draw_line("corner", leftEdgePoint, topEdgePoint, self.lineWidth, "silkscreen")
            
        # Finish plotting (clean-up and return data)
        return self.finish_plotter()
    
    def _draw_rectangle_outline(self, name, upperLeft, lowerRight, lineWidth, layer):
        ulx, uly = upperLeft
        lrx, lry = lowerRight
        
        rectWidth = lrx - ulx
        rectHeight = uly - lry
        
        # Top segment
        self.draw_line(name+"_1", (ulx, uly), (ulx + rectWidth, uly), lineWidth, layer)
        # Left segment
        self.draw_line(name+"_2", (ulx, uly), (ulx, uly - rectHeight), lineWidth, layer)
        # Bottom segment
        self.draw_line(name+"_3", (ulx, uly - rectHeight), (ulx + rectWidth, uly - rectHeight), lineWidth, layer)
        # Right segment
        self.draw_line(name+"_4", (ulx + rectWidth, uly), (ulx + rectWidth, uly - rectHeight), lineWidth, layer)
    
    def _rotate(self, point, theta):
        """
        Rotate a "point" (x,y) tuple by "theta" radians, returning
        a new tuple (newX, newY)
        """
        x,y = point
        newX = x * math.cos(theta) - y * math.sin(theta)
        newY = x * math.sin(theta) + y * math.cos(theta)
        return (newX, newY)
        
    def _rotate_part(self):
        """
        Mutate the geometry data to rotate the part so that
        the pin A1 corner is NW, respecting standard part orientation
        as per IEC 61188-7 Level A. This resolves issue #1 in 
        tracker.
        """
        # Rotation table, assuming (correctly) a 0,0 origin and pin A1 in NW corner
        partRotation = {"NW" : 0.0, "NE" : (math.pi / 2.0), "SE" : math.pi, "SW" : (3.0 * math.pi) / 2.0}
        
        # Dimensions swap table: equivalent to body rotation
        mustSwapWidthHeight = {"NE": True, "NW" : False, "SW" : True, "SE" : False}

        # Rotate all balls so that pin A1 is in the NW corner
        theta = partRotation[self.pinA1Corner]
        newBallList = []
        for ball in self.ballList:
            name, x, y, diameter = ball
            (x, y) = self._rotate((x, y), theta)
            newBallList.append((name, x, y, diameter))
        self.ballList = newBallList
        
        # Rotate pin A1 position
        self.pinA1Point = self._rotate(self.pinA1Point, theta)
        
        # Swap dimensions to simulate outline rotation following balls rotation
        if mustSwapWidthHeight[self.pinA1Corner]:
            self.packageHeight, self.packageWidth = (self.packageWidth, self.packageHeight)
                