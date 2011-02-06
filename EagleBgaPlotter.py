from BgaPlotter import *

class EagleBgaPlotter(BgaPlotter):
    def __init__(self, ballList, localValues):
        """
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
