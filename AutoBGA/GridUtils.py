"""
Miscellaneous utility functions.

Created on: Feb 19, 2011
Author: Tennessee Carmel-Veilleux (tcv -at- ro.boto.ca)
Revision: $Rev$

Copyright 2011 Tennessee Carmel-Veilleux

Description: 
Miscellaneous utility functions. These include functions to get
a temporary filename for the output image and the function to
plot the output image with grid overlay.

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
import os
import warnings
import Image
import ImageChops
import ImageDraw

def get_bin_bounds(image, nx, ny, xIdx, yIdx):
    """
    Returns (xmin, ymin, xmax, ymax) inclusive coordinates of 
    a rectangle covering the bounds of a bin.
    
    Parameters:
    * image: source image (for its size)
    * nx: number of bins on X axis in image
    * ny: number of bins on Y axis in image
    * xIdx: x axis index of bin whose bounds we want
    * yIdx: y axis index of bin whose bounds we want
    """
    sx, sy = image.size

    # Get x range for bin
    xmin = int(math.floor((float(xIdx) * sx) / nx))
    xmax = int(math.floor((float(xIdx + 1) * sx) / nx)) - 1
    if xmax >= sx: xmax = (sx - 1)

    # Get y range for bin
    ymin = int(math.floor((float(yIdx) * sy) / ny))
    ymax = int(math.floor((float(yIdx + 1) * sy) / ny)) - 1
    if ymax >= sy: ymax = (sy - 1)

    return (xmin, ymin, xmax, ymax)

def point_to_idx(image, px, py, nx, ny):
    """
    Get the ball array (x,y) bin index from a pixel
    position within the source image.
    
    Parameters:
    * image: source image (for its size)
    * px: X pixel position to query
    * py: Y pixel position to query
    * nx: number of bins on X axis in image
    * ny: number of bins on Y axis in image
    """
    sx, sy = image.size
    xIdx = int(math.floor((float(px) / float(sx)) * float(nx)))
    yIdx = int(math.floor((float(py) / float(sy)) * float(ny)))
    return (xIdx, yIdx)
    
def get_temp_filename():
    """
    Return a temporary filename to use for drawing grid images
    """
    # Disable pesky warnings about os.tempnam()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        # Save the bins image in a temporary file
        filename = os.tempnam("autobga","tmpoutimg") + ".png"
    
    return filename

def draw_bins(filename, sourceImage, nx, ny, bgaArray):
    """
    Draw an image containing the bins and detected ball positions, for
    user verification.
    
    Parameters:
    * filename: filename to use for saving processed image
    * sourceImage: source image that was processed to extract the bga array
    * nx: number of bins on X axis in image
    * ny: number of bins on Y axis in image
    * bgaArray: boolean array of occupied ball positions
    """
    # Get a new drawing context
    newImage = sourceImage.copy()
    newImage = ImageChops.invert(newImage).convert("RGB")
    gc = ImageDraw.Draw(newImage)
    sx, sy = newImage.size
    
    # Draw a circle in every detected pad bin
    for py in range(ny):
        for px in range(nx):
            xmin, ymin, xmax, ymax = get_bin_bounds(sourceImage, nx, ny, px, py)
            gc.line([(0,ymax),(sx,ymax)], fill = "blue")
            gc.line([(xmax,0),(xmax,sy)], fill = "blue")
            
            width = (xmax - xmin) + 1
            height = (ymax - ymin) + 1
            
            xmin2 = xmin + round(float(width) * 0.4)
            xmax2 = xmin + round(float(width) * 0.6)
            ymin2 = ymin + round(float(height) * 0.4)
            ymax2 = ymin + round(float(height) * 0.6)
            
            if bgaArray[py,px]:
                gc.ellipse((xmin2, ymin2, xmax2, ymax2), outline = "red", fill = "red")
    del gc
    
    try:
        newImage.save(filename)
    except IOError:
        return None    
    
    return filename