#!/usr/bin/python
# -*- coding: cp1252 -*-
"""
Image processing core library for AutoBGA

Created on: 7/09/2010
Author: Tennessee Carmel-Veilleux (tcv -at- ro.boto.ca)
Revision: $Rev$

Copyright 2010 Tennessee Carmel-Veilleux

Description: 
This module contains the GridLoader class which does the bulk of the
image processing necessary to extract the grid of balls that are
actually present on a BGA.

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

import Image
import ImageChops
import ImageDraw
import os
from numpy import array,zeros,dtype,sum,reshape,histogram,max
from numpy import nonzero,logical_and,arange,round,mean,asarray
import math

class GridLoader:
    def __init__(self, nx, ny, filename):
        self.nx = nx
        self.ny = ny
        self.filename = filename
        self.contents = zeros((ny, nx),dtype("Float32"))
        self.xSpread = zeros((ny, nx),dtype("Float32"))
        self.ySpread = zeros((ny, nx),dtype("Float32"))
        self.bgaArray = zeros((ny, nx),dtype("Float32"))

    def analyzeBin(self, binData):
        """
        Calculates pixel contents, x spread and y spread based on a single bin
        of data.
        """

        binaryBin = binData > 127

        height, width = binData.shape
        nPixels = width * height

        # Calculate spread by "flattening" in each axis
        xSpread = 0
        ySpread = 0
        xSpreadMask = zeros((1,width))
        ySpreadMask = zeros((height,1))

        for y in range(height):
            xSpreadMask[0,:] += binaryBin[y,:]

        for x in range(width):
            ySpreadMask[:,0] += binaryBin[:,x]

        xSpread = float(sum(xSpreadMask[0,:] > 1)) / width
        ySpread = float(sum(ySpreadMask[:,0] > 1)) / height

        # Find number of pixels enabled in bin
        contents = float(sum(sum(binaryBin))) / nPixels

        return (xSpread, ySpread, contents)
        #print "xSpread=%d, ySpread=%d, contents=%d" % (xSpread, ySpread, contents)

    def getBinBounds(self, xIdx, yIdx):
        sx, sy = self.image.size

        # Get x range for bin
        xmin = int(math.floor((float(xIdx) * sx) / self.nx))
        xmax = int(math.floor((float(xIdx + 1) * sx) / self.nx)) - 1
        if xmax >= sx: xmax = (sx - 1)

        # Get y range for bin
        ymin = int(math.floor((float(yIdx) * sy) / self.ny))
        ymax = int(math.floor((float(yIdx + 1) * sy) / self.ny)) - 1
        if ymax >= sy: ymax = (sy - 1)

        return (xmin, ymin, xmax, ymax)

    def eliminateCross(self, binData):
        """
        Blank-out horizontal and vertical crosslines by
        detecting rows or columns with more than 70% of their
        pixels lit and clearing them.
        
        Returns: a new clean bin data array
        """
        height, width = binData.shape
        
        newBinData = binData.copy()
        binaryBin = newBinData > 127
        
        for vLineIdx in range(width):
            if sum(binaryBin[:,vLineIdx]) > (float(height) * 0.8):
                newBinData[:,vLineIdx] = 0

        for hLineIdx in range(height):
            if sum(binaryBin[hLineIdx,:]) > (float(width) * 0.8):
                newBinData[hLineIdx,:] = 0
                
        return newBinData

    def extractBins(self):
        """
        Extract the data for all bins. Bins are rectangles whose
        sizes are approximately (imageSize / nBalls) in each dimension.

        For each bin, we determine the "spread" in X and Y and the number
        of black pixels (contents). The spread is the extent of black pixel
        within the bin, inconsiderate of the shape.

        All values extracted are normalized so that bins of different sizes
        (because of non-integer pixels/bin) don't affect the result.
        """
        # Analyze all bins
        for xIdx in range(self.nx):
            for yIdx in range(self.ny):
                # Extract bin from image
                xmin, ymin, xmax, ymax = self.getBinBounds(xIdx, yIdx)                
                binData = asarray(self.image.crop((xmin, ymin, xmax+1, ymax+1)))

                # Calculate spread and contents (number of black pixels)
                xSpread, ySpread, contents = self.analyzeBin(binData)
                
                # Eliminate center alignment crosses that could be in
                # empty bin
                if xSpread >= 0.8 and ySpread >= 0.8:
                    binData = self.eliminateCross(binData)
                    
                    # Recalculate values
                    xSpread, ySpread, contents = self.analyzeBin(binData)

                # Eliminate bins containing only either horizontal or 
                # vertical line segments
                if xSpread < 0.2 or ySpread < 0.2:
                    contents = 0
                                        
                # Save data
                self.contents[yIdx, xIdx] = contents
                self.xSpread[yIdx, xIdx] = xSpread
                self.ySpread[yIdx, xIdx] = ySpread

    def getThreshold(self, contents):
        N, M = contents.shape	
        flatContents = reshape(contents, (1,(N * M)))
        n = N * M

        (H, bins) = histogram(flatContents[0,:],64)
        H = H * 1.0

        lmax = max(flatContents[0,:])

        # Étape 1: calcul de l'histogramme normalisé
        hist_pi = (H / (M * N))

        # Étape 4: Calcul de m_g (eq 10.3-9)
        m_g = sum(arange(64) * hist_pi)

        p1_k = zeros((1,64), dtype("Float32"))
        m_k = zeros((1,64), dtype("Float32"))
        var_B = zeros((1,64), dtype("Float32"))

        for k in range(64):
            # Étape 2: Calcul de p1(k) (eq 10.3-4)
            a = sum(hist_pi[0:k])
            p1_k[0,k] = a

            # Étape 3: Calcul de m(k) (eq 10.3-8)
            m_k[0,k] = sum(arange(k) * hist_pi[0:k])

        # Étape 5: Calcul de var_B(k) (eq 10.3-17)
        denom = (p1_k * (1-p1_k))
        denom[nonzero(denom == 0)] = 1 # Élimination des dénominateurs nuls
        var_B = ((m_g * p1_k - m_k) ** 2.0) / denom


        # Étape 6: Calcul de k* à partir des maxima de var_B
        maxval = max(max(var_B));
        maxidx = nonzero(logical_and(var_B >= (maxval * 0.99999), var_B <= (maxval * 1.00001)))[1]

        k_star = round(mean(maxidx-1))/n;
        return k_star

    def extractArrayFromBins(self):

        #binAvg = average(flatContents)
        threshold = self.getThreshold(self.contents)
        self.bgaArray = self.contents >= threshold
        
    def drawBins(self):
        # Get a new drawing context
        newImage = self.image.copy()
        newImage = ImageChops.invert(newImage).convert("RGB")
        gc = ImageDraw.Draw(newImage)
        sx, sy = newImage.size
        
        # Draw a circle in every detected pad bin
        for py in range(self.ny):
            for px in range(self.nx):
                xmin, ymin, xmax, ymax = self.getBinBounds(px, py)
                gc.line([(0,ymax),(sx,ymax)], fill = "blue")
                gc.line([(xmax,0),(xmax,sy)], fill = "blue")
                
                width = (xmax - xmin) + 1
                height = (ymax - ymin) + 1
                
                xmin2 = xmin + round(float(width) * 0.4)
                xmax2 = xmin + round(float(width) * 0.6)
                ymin2 = ymin + round(float(height) * 0.4)
                ymax2 = ymin + round(float(height) * 0.6)
                
                if self.bgaArray[py,px]:
                    gc.ellipse((xmin2, ymin2, xmax2, ymax2), outline = "red", fill = "red")
        del gc
        
        # Save the bins image in a temporary file
        filename = os.tempnam("autobga","tmpoutimg") + ".png"
        try:
            newImage.save(filename)
        except IOError:
            return None    
        
        return filename
        
    def process(self):
        # Try to open image and convert it to black and white
        try:
            self.image = ImageChops.invert(Image.open(self.filename).convert("L"))
            #self.image.save("testroboto.png")
        except IOError(e):
            return (False, str(e), None)
        
        # Extract bins to internal data structures
        self.extractBins()

        # Extract BGA array geometry from bins
        self.extractArrayFromBins()
        
        tempFilename = self.drawBins()
        
        return (True, tempFilename, self.bgaArray.copy())

                #print "Bin (%d, %d): (%d %d)-(%d %d), w=%d, h=%d, n=%d" % (xIdx, yIdx, xmin, ymin, xmax, ymax, width, height, (width * height))
                #if xIdx == yIdx == 0:
                    #for py in range(height):
                        #for px in range(width):
                            #if binData[py,px] > 127:
                                #print " ",
                            #else:
                                #print "#",
                        #print

if __name__ == "__main__":
    loader = GridLoader(45,45,"C:\\Users\\veilleux\\Desktop\\Dossiers Ouverts\\autobga\\bga2.png")
    loader.process()