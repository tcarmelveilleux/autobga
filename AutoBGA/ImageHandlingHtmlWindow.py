#!/bin/env python
# -*- coding: cp1252 -*-
"""
HtmlWindow derived class that adds support for detection of click
coordinates in the BGA results image.

Created on: Feb 19, 2011
Author: Tennessee Carmel-Veilleux (tcv -at- ro.boto.ca)
Revision: $Rev$

Copyright 2011 Tennessee Carmel-Veilleux

Description: 
HtmlWindow derived class that adds support for detection of click
coordinates in the BGA results image. Assumes the image is wrapped
in a link, so that the onLinkClicked() method uses the last clicked
coordinate from the last onCellClicked() event.

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
import  wx
import  wx.html as  html

class ImageHandlingHtmlWindow(html.HtmlWindow):
    def __init__(self, parent, id, pos, size, style):
        html.HtmlWindow.__init__(self, parent, id, pos, size, style = style | wx.NO_FULL_REPAINT_ON_RESIZE)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()
        
        self.owner = None
        
        # Last clicked coordinate in image
        self.lastCoord = None
        # Size of last cell clicked
        self.lastCellSize = None
        
    def SetOwner(self, owner):
        self.owner = owner
        
    def OnLinkClicked(self, linkinfo):
        href = linkinfo.GetHref() 
        if href != "resultImage":
            # Regular link: handle through parent
            super(ImageHandlingHtmlWindow, self).OnLinkClicked(linkinfo)
        else:
            # Image link: Tell parent that image was clicked
            if self.lastCoord != None and self.lastCellSize != None:
                self.owner.onImageClicked(self.lastCoord, self.lastCellSize)

    def OnCellClicked(self, cell, x, y, evt):
        # Record data about the click for the OnLinkClicked() method
        self.lastCoord = (x, y)
        self.lastCellSize = (cell.GetWidth(), cell.GetHeight())
        
        # Also run default handler in case
        super(ImageHandlingHtmlWindow, self).OnCellClicked(cell, x, y, evt)
