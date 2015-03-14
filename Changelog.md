# Change log for AutoBGA #
## v1.2, released February 28, 2011 ##
  * FEATURE: Silkscreen outline and courtyard drawing now implemented
  * FEATURE: Automatic rotation to have pin A1 in NW corner (IPC profile 1)
  * FEATURE: Can now click in detected pads image to toggle balls
  * FEATURE: Added "Export to clipboard" and "Export to file..." buttons
  * IMPROVEMENT: Better validation of package dimensions
  * IMPROVEMENT: Can export to new format without recomputing
  * IMPROVEMENT: Simpler user interface
  * IMPROVEMENT: Better heuristics for removing crosses especially in the case of misaligned, high-resolution images
  * BUGFIX: XML output bug where some attributes were missing in the FootprintLibrary element which made the file invalid according to the FootprintLibrary schema
  * BUGFIX: Vertical positioning bug in the ball position generator that caused a shift down of the center position when width was not the same as height

## v1.1, released January 16, 2011 ##
  * IMPROVEMENT: Better cross and line removal in images.
  * FEATURE: Added a second thresholding algorithm better-suited for cases with high-resolution and fine lines. This has fixed numerous cases of improper ball detection that were present in version 1.0.
  * IMPROVEMENT: Smaller UI footprint owing to displacement of parameters from top of window to a separate tab.
  * IMPROVEMENT: Automatically switches to results tab after computing.

## v1.0, released September 13, 2010 ##
  * Initial release.
  * Works as advertised, but still some sub-optimal cases where cleaning-up of images is required.