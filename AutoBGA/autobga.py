#!/bin/env python
# -*- coding: cp1252 -*-
"""
AutoBGA main user interface

Created on: 7/09/2010
Author: Tennessee Carmel-Veilleux (tcv -at- ro.boto.ca)
Revision: $Rev$

Copyright 2010 Tennessee Carmel-Veilleux

Description: 
Main user interface for AutoBGA

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

import os
import sys
import GridLoader
import BgaPadNameGenerator
import wx
import wx.html as html

from autobga_wdr import *

VERSION = "1.0"

# WDR: classes

class AboutDialog(wx.Dialog):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.DEFAULT_DIALOG_STYLE ):
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)
        
        # WDR: dialog function AboutDialog for AboutDialog
        AboutDialogFunc( self, True )
        
        self.getHtmlAbout().SetPage("""<html><body>
        <div align="center">
        <h3><img src="%s" align="right">AutoBGA v%s ($Rev$)</h3>
        <p>&copy; Copyright 2010 Tennessee Carmel-Veilleux</p>
        <p>For any bug reports or suggestions, contact me at:
        tcv(at)ro.boto.ca
        or visit <a href="http://code.google.com/p/autobga/">http://code.google.com/p/autobga/</a></p>
        </div>
        </body></html>""" % (wx.FileSystem.FileNameToURL(parent.progDir + "/doc/autobga_logo.png"), VERSION))
        
        # WDR: handler declarations for AboutDialog

    # WDR: methods for AboutDialog

    def getHtmlAbout(self):
        return self.FindWindowById( ID_HTML_ABOUT )

    # WDR: handler implementations for AboutDialog


class MainPanel(wx.Panel):
    def __init__(self, parent, id,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER):
        wx.Panel.__init__(self, parent, id, pos, size, style)
                
        self.initLocalData()
                
        MainDialog(self, True)
        
        self.getHtmlReport().SetPage("<html><body><H3>No results yet !</H3></body></html>")
        
        self.progDir = parent.progDir
        self.getHtmlHelp().LoadPage(wx.FileSystem.FileNameToURL(self.progDir + "/doc/index.html"))
        
        self.getTextCtrlFilename().SetValue(os.path.normpath(self.progDir + "/example_bga.png"))
        # self.displayInfo("argv0: %s\nprogDir: %s\nexample:%s\nhelp:%s" % (sys.argv[0], self.progDir, os.path.normpath(self.progDir + "/example_bga.png"), wx.FileSystem.FileNameToURL(self.progDir + "/doc/index.html")))
        
        self.getChoiceFormat().SetStringSelection("EAGLE SCR")
        self.getChoicePictureView().SetStringSelection("Bottom")
        self.getChoicePinA1().SetStringSelection("SE")
        
        # WDR: handler declarations for MainPanel
        wx.EVT_BUTTON(self, ID_BUTTON_COMPUTE, self.onCompute)
        wx.EVT_BUTTON(self, ID_BUTTON_BROWSE, self.onBrowse)
        
    # WDR: methods for MainPanel
    
    def getTextCtrlPadDiameter(self):
        return self.FindWindowById( ID_TEXTCTRL_PADDIAMETER )

    def getTextCtrlPackHeight(self):
        return self.FindWindowById( ID_TEXTCTRL_PACKHEIGHT )

    def getTextCtrlPackWidth(self):
        return self.FindWindowById( ID_TEXTCTRL_PACKWIDTH )

    def getChoiceFormat(self):
        return self.FindWindowById( ID_CHOICE_FORMAT )

    def getChoicePictureView(self):
        return self.FindWindowById( ID_CHOICE_PICTURE_VIEW )

    def getChoicePinA1(self):
        return self.FindWindowById( ID_CHOICE_PIN_A1 )

    def getButtonCompute(self):
        return self.FindWindowById( ID_BUTTON_COMPUTE )

    def getHtmlReport(self):
        return self.FindWindowById( ID_HTML_REPORT )

    def getHtmlHelp(self):
        return self.FindWindowById( ID_HTML_HELP )

    def getTextCtrlPitch(self):
        return self.FindWindowById( ID_TEXTCTRL_PITCH )

    def getTextCtrlBallHeight(self):
        return self.FindWindowById( ID_TEXTCTRL_BALLHEIGHT )

    def getTextCtrlBallWidth(self):
        return self.FindWindowById( ID_TEXTCTRL_BALLWIDTH )

    def getButtonBrowse(self):
        return self.FindWindowById( ID_BUTTON_BROWSE )

    def getTextCtrlFilename(self):
        return self.FindWindowById( ID_TEXTCTRL_FILENAME )
    
    # WDR: handler implementations for MainPanel
        
    def initLocalData(self):
        self.localValues = {"width" : 0, 
                            "height" : 0, 
                            "pitch" : 0.0,
                            "padDiameter" : 0.0,
                            "pinA1Corner" : "SE",
                            "outputFormat" : "EAGLE SCR",
                            "pictureView" : "Bottom",
                            "inFilename" : ""}
        
    def highlight(self, textCtrl):
        """
        Highlight and set focus to a text control, to show an error.
        """
        textCtrl.SetBackgroundColour("pink")
        textCtrl.SetFocus()
        textCtrl.Refresh()
    
    def unhighlight(self, textCtrl):
        """
        Unhighlight a text control, to clear an error indication.
        """
        textCtrl.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        textCtrl.Refresh()
        
    def displayError(self, message):
        dlg = wx.MessageDialog(self, message, 'Error...', wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        
    def displayInfo(self, message):
        dlg = wx.MessageDialog(self, message, 'Information...', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
    def validateIntInRange(self, labelText, textCtrl, minValue, maxValue):
        """
        Validates that text control "textCtrl" contains an integer value
        between [minValue, maxValue]. If it doesn't, an error dialog is shown
        that mentions the name of the field as "labelText".
        
        Returns: a tuple (isValid, value).
        """
        if textCtrl.IsEmpty():
            self.highlight(textCtrl)
            self.displayError("Value of field '%s' can't be empty !" % labelText)
            return (False, 0)
        
        value = 0
        try:
            value = int(textCtrl.GetValue())
            if value < minValue or value > maxValue:
                raise ValueError
        except ValueError:
            self.highlight(textCtrl)
            self.displayError("Value of field '%s' must be between %d and %d !" % (labelText, minValue, maxValue))
            return (False, 0)
        
        self.unhighlight(textCtrl)
        return (True, value)
    
    def validateFloatInRange(self, labelText, textCtrl, minValue, maxValue):
        """
        Validates that text control "textCtrl" contains a float value
        between [minValue, maxValue]. If it doesn't, an error dialog is shown
        that mentions the name of the field as "labelText".
        
        Returns: a tuple (isValid, value).
        """
        if textCtrl.IsEmpty():
            self.highlight(textCtrl)
            self.displayError("Value of field '%s' can't be empty !" % labelText)
            return (False, 0)
        
        value = 0.0
        try:
            value = float(textCtrl.GetValue())
            if value < minValue or value > maxValue:
                raise ValueError
        except ValueError:
            self.highlight(textCtrl)
            self.displayError("Value of field '%s' must be between %.3f and %.3f !" % (labelText, minValue, maxValue))
            return (False, 0)
        
        self.unhighlight(textCtrl)
        return (True, value)
    
    def validateControls(self):
        (isValid, width) = self.validateIntInRange("Width", self.getTextCtrlBallWidth(), 1, 200)
        if not isValid: return False
        
        (isValid, height) = self.validateIntInRange("Height", self.getTextCtrlBallHeight(), 1, 200)
        if not isValid: return False
            
        (isValid, pitch) = self.validateFloatInRange("Pitch", self.getTextCtrlPitch(), 0.1, 2.0)
        if not isValid: return False

        (isValid, padDiameter) = self.validateFloatInRange("Pad diameter", self.getTextCtrlPadDiameter(), 0.05, 2.0)
        if not isValid: return False

        if not os.path.exists(self.getTextCtrlFilename().GetValue()):
            self.highlight(self.getTextCtrlFilename())
            self.displayError("Input file '%s' does not exists !" % self.getTextCtrlFilename().GetValue())
            return False
        else:
            self.unhighlight(self.getTextCtrlFilename())
            inFilename = self.getTextCtrlFilename().GetValue()

        pinA1Corner = self.getChoicePinA1().GetStringSelection()
        pictureView = self.getChoicePictureView().GetStringSelection()
        outputFormat = self.getChoiceFormat().GetStringSelection()
        
        # We got here: all controls are valid, store data
        for key, value in locals().items():
            if key in self.localValues:
                self.localValues[key] = value
                
        return True
    
    def _getPosition(self, x, y, width, height, pitch):
        if (width % 2) == 0:
            # Even width:
            minX = -(float((width / 2) - 1) + 0.5) * pitch
        else:
            # Odd width:
            minX = -(float((width - 1) / 2)) * pitch

        if (height % 2) == 0:
            # Even height:
            minY = float((width / 2) - 1) + 0.5 * pitch
        else:
            # Odd width:
            minY = float((width - 1) / 2) * pitch
            
        xPos = (minX + (float(x) * pitch))
        yPos = (minY - (float(y) * pitch))
        return (xPos, yPos)

        
    def _copyToClipboard(self, text, message):
        if not wx.TheClipboard.IsOpened():
            if sys.platform == 'win32':
                cleanText = text.replace("\n","\r\n")
            else:
                cleanText = text
            clipdata = wx.TextDataObject()
            clipdata.SetText(cleanText)
            wx.TheClipboard.Open()
            wx.TheClipboard.SetData(clipdata)
            wx.TheClipboard.Close()
            self.displayInfo(message)
            return True
        else:
            self.displayError("Error accessing the clipboard :(\nResult lost. Please retry.")
            return False
        
    def _outputTSV(self, ballList):
        tsvList = []
        tsvList.append("Pad name\tX position (mm)\tY position (mm)\tPad diameter (mm)")
        tsvList.extend(["%s\t%.3f\t%.3f\t%.3f" % ball for ball in ballList])
        resultString = "\n".join(tsvList)
        return self._copyToClipboard(resultString, "Success: TSV data copied to clipboard !")
            
    def _outputEAGLE(self, ballList):
        # ball[0] = name
        # ball[1] = X
        # ball[2] = y
        # ball[3] = diameter
        eagleList = []
        eagleList.append("change style continuous;\ngrid mm;\nset wire_bend 2;\nlayer 1;")
        eagleList.extend(["smd %.3f %.3f -100 '%s' (%.3f %.3f);" % (ball[3], ball[3], ball[0], ball[1], ball[2]) for ball in ballList])
        eagleList.append("grid last;");
        resultString = "\n".join(eagleList)
        return self._copyToClipboard(resultString, "Success: EAGLE Script data copied to clipboard !")
        
    def _outputXML(self, ballList):
        xmlList = []
        xmlList.append("""<?xml version="1.0" encoding="UTF-8"?>
<footprintLibrary xmlns="http://www.tentech.ca/schemas/FootprintLibrary"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <description>Single footprint generated with AutoBGA</description>
    <footprints>
        <footprint name="bga_%(width)d_%(height)d">
            <description>BGA%(width)d x %(height)d balls, %(pitch).3f mm pitch</description>
            <geometry>
            """ % self.localValues)
        
        xmlList.extend(['<padElement name="%s" layer="topLayer" thickness="0" xPos="%.3f" yPos="%.3f" width="%.3f" height="%.3f" angle="0" padShape="circle" maxTextHeight="%.3f"/>' % (ball[0], ball[1], ball[2], ball[3], ball[3], 0.8*ball[3]) for ball in ballList])
        xmlList.append("""
            </geometry>
        </footprint>
    </footprints>
</footprintLibrary>""")
        resultString = "\n".join(xmlList)
        return self._copyToClipboard(resultString, "Success: XML data copied to clipboard !")
        
                
    def _outputGrid(self, grid):
        """
        Outputs the BGA grid in the selected file format and
        returns a string containing an HTML table of the resulting footprint. 
        """
        
        # Generate pad names now
        nameGenerator = BgaPadNameGenerator.BgaPadNameGenerator(grid.shape[1], grid.shape[0], self.localValues["pinA1Corner"])        
        padNames = nameGenerator.generatePadNames()

        # Mirror along the vertical axis (flip horizontally) if picture was bottom view
        if self.localValues["pictureView"].upper() == "BOTTOM":
            flippedGrid = grid[:,::-1]
        else:
            flippedGrid = grid
        
        # Create list of pads
        resultList = []
        height, width = grid.shape
        pitch = self.localValues["pitch"]
        padDiameter = self.localValues["padDiameter"]

        for yIdx in xrange(height):
            for xIdx in xrange(width):
                if flippedGrid[yIdx, xIdx]:
                    xPos, yPos = self._getPosition(xIdx, yIdx, width, height, pitch)
                    resultList.append((padNames[xIdx][yIdx], xPos, yPos, padDiameter))

        # Create display table
        tableList = ['<font size="-2"><table border="1">']
        for yIdx in xrange(height):
            tableList.append("<tr>")
            for xIdx in xrange(width):
                padName = padNames[xIdx][yIdx]
                
                if flippedGrid[yIdx, xIdx]:
                    # Ball present
                    if padName == "A1":
                        color = "Red"
                    else:
                        color = "Cyan"
                        
                    tableList.append('<td bgcolor="%s">%s</td>' % (color, padName))
                else:
                    # Ball absent
                    if padName == "A1":
                        tableList.append('<td bgcolor="red"></td>')
                    else:
                        tableList.append('<td></td>')
                    
            tableList.append("</tr>")
        tableList.append("</table></font>")
        
        # Call correct handler
        if self.localValues["outputFormat"] == "EAGLE SCR":
            self._outputEAGLE(resultList)
        elif self.localValues["outputFormat"] == "XML":
            self._outputXML(resultList)
        elif self.localValues["outputFormat"] == "TSV (Excel)":
            self._outputTSV(resultList)
            
        return "".join(tableList)
            
    def onCompute(self, event):
        # Validate controls and transfer values to self.localValues
        if not self.validateControls():
            return
        
        # Appear busy
        self.getButtonBrowse().Enable(False)
        self.getButtonCompute().Enable(False)
        wx.BeginBusyCursor()
        
        # Process grid
        gridLoader = GridLoader.GridLoader(self.localValues["width"], self.localValues["height"],
                                           self.localValues["inFilename"])
        (success, strValue, bgaArray) = gridLoader.process()

        # Stop appearing busy        
        wx.EndBusyCursor()

        self.getButtonBrowse().Enable(True)
        self.getButtonCompute().Enable(True)

        # Display results
        if not success:
            page = "<html><body><h1>Error: '%s' !</h1></body></html>" % strValue
        else:
            self.localValues["table"] = self._outputGrid(bgaArray)
            self.localValues["outFilename"] = wx.FileSystem.FileNameToURL(strValue)
            page = """
            <html><body>
            <h1>Results</h1>
            <p><u>Table of contents</u></p>
            <ul>
            <li><a href="#input">Input image preview</a></li>
            <li><a href="#detected">Pads detected</a></li>
            <li><a href="#table">Table representation of output</a></li>
            </ul>
            <a name="input"></a>
            <h2>Input image:</h2>
            <p><img src="%(inFilename)s"></p>
            <a name="detected"></a>            
            <h2>Pads detected overlay (red dots):</h2>
            <p><img src="%(outFilename)s"></p>
            <a name="table">
            <h2>Table representation of output footprint (from top):</h2>
            <p>%(table)s</p>
            </body></html>""" % self.localValues
            
        self.getHtmlReport().SetPage(page)
        self.getHtmlReport().Scroll(0, 0)

    def onBrowse(self, event):
        """
        Browse for image files. Can only select existing files.
        """
        wildcard = "PNG files (*.png)|*.png|BMP files (*.bmp)|*.bmp"
        
        fileDialog = wx.FileDialog(
            self, message="Choose an input image...",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR | wx.FD_FILE_MUST_EXIST 
            )

        if fileDialog.ShowModal() == wx.ID_OK:
            filename = fileDialog.GetPath()
            self.getTextCtrlFilename().SetValue(filename)

        fileDialog.Destroy()
    
class MainFrame(wx.Frame):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.DEFAULT_FRAME_STYLE ):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        # Find-out where we are, to generate filenames
        self.progDir = os.path.normpath(os.path.dirname(sys.argv[0]))
        
        self.CreateMyMenuBar()
        
        # insert main window here        
        self.panel = MainPanel(self,-1)
        self.panel.Fit()
        self.Fit()
        
        # Setting our own icon from file, as seen on the wxPyWiki:
        # http://wiki.wxpython.org/LoadIconFromWin32Resources
        
        # set window icon
        if sys.platform == 'win32':
            # only do this on windows, so we don't
            # cause an error dialog on other platforms
            exeName = sys.executable
            icon = wx.Icon(exeName, wx.BITMAP_TYPE_ICO)
            self.SetIcon(icon)
            
        # WDR: handler declarations for MainFrame
        wx.EVT_MENU(self, wx.ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnQuit)
        wx.EVT_CLOSE(self, self.OnCloseWindow)
        
    # WDR: methods for MainFrame

    def CreateMyMenuBar(self):
        self.SetMenuBar( MyMenuBarFunc() )
    
    # WDR: handler implementations for MainFrame
        
    def OnAbout(self, event):
        dialog = AboutDialog(self, -1, "About AutoBGA v%s" % VERSION)
        dialog.CentreOnParent()
        dialog.ShowModal()
        dialog.Destroy()
    
    def OnQuit(self, event):
        self.Close(True)
    
    def OnCloseWindow(self, event):
        self.Destroy()
        
#----------------------------------------------------------------------------

class AutoBGAApplication(wx.App):
    
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame = MainFrame( None, -1, "AutoBGA", [20,20], [500,340] )
        frame.Show(True)

        return True

#----------------------------------------------------------------------------

app = AutoBGAApplication(False)
app.MainLoop()

