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
