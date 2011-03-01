mkdir autobga-sources-v1.2
mkdir autobga-sources-v1.2\doc
mkdir autobga-sources-v1.2\icons

cp -f autobga.wdr autobga.wpr example_bga.png autobga.py autobga_wdr.py BgaPadNameGenerator.py BgaPlotter.py EagleBgaPlotter.py ExternalBrowserHtmlWindow.py GridLoader.py GridUtils.py ImageHandlingHtmlWindow.py TSVBgaPlotter.py XMLBgaPlotter.py installer-script.nsi LICENSE.txt makeexe.bat setup.py autobga-sources-v1.2
cp -f doc\adobe_reader_snapshot_tool.png doc\autobga_logo.png doc\foxit_picture_tool.png doc\index.html doc\sample_pdf_steps.png autobga-sources-v1.2\doc
cp -f icons\autobga.ico icons\bga-tool-16.png icons\bga-tool-32.png icons\bga-tool-64.png autobga-sources-v1.2\icons
zip -9 -r autobga-sources-v1.2.zip ./autobga-sources-v1.2
rm -rf autobga-sources-v1.2