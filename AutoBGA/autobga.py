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
import EagleBgaPlotter
import TSVBgaPlotter
import XMLBgaPlotter
from GridUtils import *

from autobga_wdr import *

VERSION = "1.2"

def getProgDir():
    # Find-out where we are, to generate filenames
    return os.path.normpath(os.path.dirname(sys.argv[0]))

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
        </body></html>""" % (wx.FileSystem.FileNameToURL(getProgDir() + "/doc/autobga_logo.png"), VERSION))
        
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
        
        # Make notebook have a non-white background color under Windows XP+
        notebook = self.getNotebook()
        col = notebook.GetThemeBackgroundColour()
        if col and col.Ok():
            for pageIdx in xrange(notebook.GetPageCount()):
                notebook.GetPage(pageIdx).SetBackgroundColour(col)

        # Initialize results report
        self.getHtmlReport().SetPage("<html><body><H3>No results yet !</H3></body></html>")
        self.getHtmlReport().SetOwner(self)
        
        # Load help in help panel
        self.getHtmlHelp().LoadPage(wx.FileSystem.FileNameToURL(getProgDir() + "/doc/index.html"))

        # Initialize all configuration fields
        self.getTextCtrlFilename().SetValue(os.path.normpath(getProgDir() + "/example_bga.png"))
        # self.displayInfo("argv0: %s\nprogDir: %s\nexample:%s\nhelp:%s" % (sys.argv[0], getProgDir(), os.path.normpath(getProgDir() + "/example_bga.png"), wx.FileSystem.FileNameToURL(getProgDir() + "/doc/index.html")))
        
        self.getChoiceFormat().SetStringSelection("EAGLE SCR")
        self.getChoicePictureView().SetStringSelection("Bottom")
        self.getChoicePinA1().SetStringSelection("SE")
        
        self.fileFormatExtensions = {"EAGLE SCR" : "*.scr", "XML" : "*.xml", "TSV (Excel)" : "*.tsv"}
        
        # WDR: handler declarations for MainPanel
        wx.EVT_BUTTON(self, ID_BUTTON_EXPORT_TO_FILE, self.onExportToFile)
        wx.EVT_BUTTON(self, ID_BUTTON_EXPORT_TO_CLIPBOARD, self.onExportToClipboard)
        wx.EVT_BUTTON(self, ID_BUTTON_COMPUTE, self.onCompute)
        wx.EVT_BUTTON(self, ID_BUTTON_BROWSE, self.onBrowse)
        
    # WDR: methods for MainPanel
    
    def getButtonExportToFile(self):
        return self.FindWindowById( ID_BUTTON_EXPORT_TO_FILE )

    def getButtonExportToClipboard(self):
        return self.FindWindowById( ID_BUTTON_EXPORT_TO_CLIPBOARD )

    def getNotebook(self):
        return self.FindWindowById( ID_NOTEBOOK )

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
                            "packageWidth" : 0.0,
                            "packageHeight" : 0.0,
                            "pitch" : 0.0,
                            "padDiameter" : 0.0,
                            "pinA1Corner" : "SE",
                            "pinA1Point" : (0.0, 0.0),
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
        """
        Validate that all parameters controls are within valid ranges and
        transfer the values to local parameter storage.
        
        If an error occurs, returns False, otherwise return True.
        
        The control in which a value error is found will be highlighted and
        focused.
        """
        (isValid, width) = self.validateIntInRange("Width (NX)", self.getTextCtrlBallWidth(), 1, 200)
        if not isValid: return False
        
        (isValid, height) = self.validateIntInRange("Height (NY)", self.getTextCtrlBallHeight(), 1, 200)
        if not isValid: return False
        
        (isValid, packageWidth) = self.validateFloatInRange("Width (A)", self.getTextCtrlPackWidth(), 0.5, 100.0)
        if not isValid: return False

        (isValid, packageHeight) = self.validateFloatInRange("Height (B)", self.getTextCtrlPackHeight(), 0.5, 100.0)
        if not isValid: return False

        (isValid, pitch) = self.validateFloatInRange("Pitch (e)", self.getTextCtrlPitch(), 0.1, 2.0)
        if not isValid: return False

        (isValid, padDiameter) = self.validateFloatInRange("Pad diameter", self.getTextCtrlPadDiameter(), 0.05, 2.0)
        if not isValid: return False

        # Make sure package dimensions are not too small compared to ball array size
        isValid = self._validateDimensions(width, height, packageWidth, packageHeight, pitch)
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
        
        # We got here: all controls are valid, store data
        for key, value in locals().items():
            if key in self.localValues:
                self.localValues[key] = value
                
        return True
    
    def _getPosition(self, x, y, width, height, pitch):
        """
        Ball position generator.
        
        Determine the (x, y) position of a ball (in mm) from an
        x,y ball index (0...width-1, 0...height-1) and the pad
        pitch.
        
        Returns (x,y), a ball position center point.
        """
        if (width % 2) == 0:
            # Even width:
            minX = -(float((width / 2) - 1) + 0.5) * pitch
        else:
            # Odd width:
            minX = -(float((width - 1) / 2)) * pitch

        if (height % 2) == 0:
            # Even height:
            minY = float((height / 2) - 1) + 0.5 * pitch
        else:
            # Odd width:
            minY = float((height - 1) / 2) * pitch
            
        xPos = (minX + (float(x) * pitch))
        yPos = (minY - (float(y) * pitch))
        return (xPos, yPos)
    
    def _validateDimensions(self, width, height, packageWidth, packageHeight, pitch):
        minPackageWidth = width * pitch
        minPackageHeight = height * pitch
        
        if packageWidth < minPackageWidth:
            self.displayError("Value of field Width (A) must be at least %.3f mm,\notherwise package outline will overlap balls." % (minPackageWidth))
            self.highlight(self.getTextCtrlPackWidth())
            return False
        
        if packageHeight < minPackageHeight:
            self.displayError("Value of field Height (B) must be at least %.3f mm,\notherwise package outline will overlap balls." % (minPackageHeight))
            self.highlight(self.getTextCtrlPackHeight())
            return False
        
        self.unhighlight(self.getTextCtrlPackWidth())
        self.unhighlight(self.getTextCtrlPackHeight())
        return True
        
    def _copyToClipboard(self, text, message):
        """
        Copy the "text" to the clipboard and then display an
        info message dialog with "message" as the contents.
        """
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
            self.displayError("Error accessing the clipboard :\nResult lost. Please retry.")
            return False
        
    def _outputTSV(self, ballList, localValues):
        plotter = TSVBgaPlotter.TSVBgaPlotter(ballList, localValues)
        resultString = plotter.process()
        return resultString
            
    def _outputEAGLE(self, ballList, localValues):
        plotter = EagleBgaPlotter.EagleBgaPlotter(ballList, localValues)
        
        try:
            resultString = plotter.process()
            if not resultString:
                self.displayError("Problem while trying to generate EAGLE data !")
                return None
        except RuntimeError, e:
            self.displayError("Problem while trying to generate EAGLE data: %s !" % str(e))
            
        return resultString
        
    def _outputXML(self, ballList, localValues):
        plotter = XMLBgaPlotter.XMLBgaPlotter(ballList, localValues, VERSION)
        
        try:
            resultString = plotter.process()
            if not resultString:
                self.displayError("Problem while trying to generate XML data !")
                return None
        except RuntimeError, e:
            self.displayError("Problem while trying to generate XML data: %s !" % str(e))
            
        return resultString
        
    def _getProcessedGrid(self, grid):
        """
        Get the processed grid ready for further output.
        
        Updates internal state related to processed grid.
        
        Returns a resultList containing the processed grid items
        with all ball names, positions and diameters.
        """
        
        # Generate pad names now
        nameGenerator = BgaPadNameGenerator.BgaPadNameGenerator(grid.shape[1], grid.shape[0], self.localValues["pinA1Corner"])        
        padNames = nameGenerator.generatePadNames()
        self.localValues["padNames"] = padNames
        
        # Mirror along the vertical axis (flip horizontally) if picture was bottom view
        if self.localValues["pictureView"].upper() == "BOTTOM":
            flippedGrid = grid[:,::-1]
        else:
            flippedGrid = grid

        self.localValues["flippedGrid"] = flippedGrid
        
        # Create list of pads to be drawn based on positions detected in grid
        resultList = []
        height, width = grid.shape
        pitch = self.localValues["pitch"]
        padDiameter = self.localValues["padDiameter"]

        for yIdx in xrange(height):
            for xIdx in xrange(width):
                xPos, yPos = self._getPosition(xIdx, yIdx, width, height, pitch)

                # Save pin A1 position even if it does not exist, for corner line drawing
                if padNames[xIdx][yIdx].upper() == "A1":
                    self.localValues["pinA1Point"] = (xPos, yPos)
                    
                # Add ball if it exists in detected grid
                if flippedGrid[yIdx, xIdx]:
                    resultList.append((padNames[xIdx][yIdx], xPos, yPos, padDiameter))

        return resultList

    def _outputGridHTML(self):
        width, height = (self.localValues["width"], self.localValues["height"])
        flippedGrid = self.localValues["flippedGrid"]
        padNames = self.localValues["padNames"]        

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
        
        return "".join(tableList)
    
    def _plotGrid(self, resultList, filename):
        """
        Generate plot data from BGA grid data in "resultList". Outputs
        to a file named "filename". If "filename" is None, output is copied
        to the clipboard.
        """
        # Call correct handler
        if self.localValues["outputFormat"] == "EAGLE SCR":
            resultStr = self._outputEAGLE(resultList, self.localValues)
        elif self.localValues["outputFormat"] == "XML":
            resultStr = self._outputXML(resultList, self.localValues)
        elif self.localValues["outputFormat"] == "TSV (Excel)":
            resultStr = self._outputTSV(resultList, self.localValues)
        
        if resultStr:
            if filename:
                try:
                    outFile = file(filename, "w+")
                    outFile.write(resultStr + "\n")
                    outFile.close()
                except IOError, e:
                    self.displayError('Error saving to file "%s":\n %s' % (filename, str(e)))
            else:
                self._copyToClipboard(resultStr, "Success: %s data copied to clipboard !" % self.localValues["outputFormat"])
    
    def _displayResults(self, success, errorMessage):
        if not success:
            page = "<html><body><h1>Error: '%s' !</h1></body></html>" % errorMessage
        else:
            # Generate BGA and output in the correct format
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
            <p>You can click on any cell of the image to toggle the ball present/absent state that was detected prior to export.
            The update is instantaneous. You do not need to click "compute" to apply the changes.</p>
            <p><a href="resultImage"><img src="%(outFilenameURL)s"></a></p>
            <a name="table">
            <h2>Table representation of output footprint (from top):</h2>
            <p>%(table)s</p>
            </body></html>""" % self.localValues
            
        self.getHtmlReport().SetPage(page)
            
    def onExportToFile(self, event):
        """
        Event handler for the "Export to file..." button.
        """
        # Obtain the output format
        outputFormat = self.getChoiceFormat().GetStringSelection()
        self.localValues["outputFormat"] = outputFormat
        wildcard = "%s (%s)|%s|All Files (*.*)|*.*" % (outputFormat, self.fileFormatExtensions[outputFormat], self.fileFormatExtensions[outputFormat])
        
        fileDialog = wx.FileDialog(
            self, message="Choose an output file...",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.SAVE | wx.FD_OVERWRITE_PROMPT
            )

        if fileDialog.ShowModal() == wx.ID_OK:
            filename = fileDialog.GetPath()
            
            # Plot result and save to file
            resultList = self._getProcessedGrid(self.localValues["bgaArray"])
            self._plotGrid(resultList, filename)
        
        fileDialog.Destroy()        

    def onExportToClipboard(self, event):
        """
        Event handler for the "Export to clipboard" button
        """
        # Plot result and save to clipboard
        self.localValues["outputFormat"] = self.getChoiceFormat().GetStringSelection()
        resultList = self._getProcessedGrid(self.localValues["bgaArray"])
        self._plotGrid(resultList, None)
        
    def onCompute(self, event):
        """
        Event handler for the "compute" button. 
        
        Steps:
        1- Calls controls validation
        2- Runs the computation to build the grid array
        3- Output the grid array
        4- Display the results page
        """
        # Validate controls and transfer values to self.localValues
        if not self.validateControls():
            return
        
        # Appear busy
        self._startBusy()

        # Create a temporary filename for the output image
        self.localValues["outImageFilename"] = get_temp_filename()
        
        # Process grid
        gridLoader = GridLoader.GridLoader(self.localValues["width"], self.localValues["height"],
                                           self.localValues["inFilename"])
        (success, errorMessage, bgaArray, sourceImage) = gridLoader.process()

        self.localValues["isComputationValid"] = success
        
        # Display results
        if not success:
            self._displayResults(success, errorMessage)
        else:
            # Store data derived from processing
            self.localValues["sourceImage"] = sourceImage
            self.localValues["bgaArray"] = bgaArray
            self.localValues["outFilename"] = get_temp_filename()
            self.localValues["outFilenameURL"] = wx.FileSystem.FileNameToURL(self.localValues["outFilename"])

            # Regenerate processed grid with all names and correct flipping
            self.localValues["resultList"] = self._getProcessedGrid(self.localValues["bgaArray"])
            
            # Generate "detected balls" image
            draw_bins(self.localValues["outFilename"], sourceImage, self.localValues["width"], self.localValues["height"], self.localValues["bgaArray"])
            
            # Draw HTML table of grid
            self.localValues["table"] = self._outputGridHTML()
            
            # Display all results       
            self._displayResults(success, "")
            
        self.getHtmlReport().Scroll(0, 0)
        # Show results page
        self.getNotebook().ChangeSelection(1)

        # Show results page
        self.getNotebook().ChangeSelection(1)
        
        self._stopBusy()
        
    def onBrowse(self, event):
        """
        Event handler for the "Browse" button.
        
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
        
    def onImageClicked(self, point, cellSize):
        """
        Event handler for a pseudo-event generated by ImageHandlingHtmlWindow.
        
        This event handler toggles a ball position based on clicks in the results image.
        The "point" parameter is the image coordinate that was clicked. The "cellSize"
        is a (width, height) tuple of the HtmlCell within which the click occured. The
        "cellSize" parameter is used to determine whether the click actually occured in
        the desired image, by matching with the expected image size.
        """
        cellWidth, cellHeight = cellSize
        sx, sy = self.localValues["sourceImage"].size
        px, py = point
        
        if sx == cellWidth and sy == cellHeight:
            self._startBusy()
            
            # Toggle ball
            xIdx, yIdx = point_to_idx(self.localValues["sourceImage"], px, py, self.localValues["width"], self.localValues["height"])
            self.localValues["bgaArray"][yIdx, xIdx] = not self.localValues["bgaArray"][yIdx, xIdx]
            prevScrollX, prevScrollY = self.getHtmlReport().GetViewStart()

            # Regenerate processed grid with all names and correct flipping
            self.localValues["resultList"] = self._getProcessedGrid(self.localValues["bgaArray"])
            
            # Regenerate "detected balls" image
            draw_bins(self.localValues["outFilename"], self.localValues["sourceImage"], self.localValues["width"], self.localValues["height"], self.localValues["bgaArray"])
            
            # Redraw HTML table of grid
            self.localValues["table"] = self._outputGridHTML()
            
            # Display results graph           
            self._displayResults(True, "")
    
            # Refresh report
            self.getHtmlReport().Scroll(prevScrollX, prevScrollY)
            self.getHtmlReport().Refresh()
            self.getHtmlReport().Update()

            self._stopBusy()

    def _startBusy(self):
        # Start appearing busy
        self.getButtonBrowse().Enable(False)
        self.getButtonCompute().Enable(False)
        self.getButtonExportToFile().Enable(False)
        self.getButtonExportToClipboard().Enable(False)
        wx.BeginBusyCursor()

    def _stopBusy(self):
        # Stop appearing busy        
        wx.EndBusyCursor()
     
        # Set button enables according to values
        self.getButtonBrowse().Enable(True)
        self.getButtonCompute().Enable(True)

        self.getButtonExportToClipboard().Enable(self.localValues["isComputationValid"])
        self.getButtonExportToFile().Enable(self.localValues["isComputationValid"])
    
class MainFrame(wx.Frame):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.DEFAULT_FRAME_STYLE ):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        
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
        frame = MainFrame( None, -1, "AutoBGA v" + VERSION + " by Tennessee Carmel-Veilleux", [20,20], [600,340] )
        frame.Show(True)

        return True

#----------------------------------------------------------------------------

app = AutoBGAApplication(False)
app.MainLoop()

