mkdir autobga-sources-v1.0
mkdir autobga-sources-v1.0\doc
mkdir autobga-sources-v1.0\icons
cp -f autobga.py autobga.wdr autobga.wpr autobga_wdr.py BgaPadNameGenerator.py example_bga.png ExternalBrowserHtmlWindow.py GridLoader.py installer-script.nsi LICENSE.txt makeexe.bat setup.py autobga-sources-v1.0
cp -f doc\adobe_reader_snapshot_tool.png doc\autobga_logo.png doc\foxit_picture_tool.png doc\index.html doc\sample_pdf_steps.png autobga-sources-v1.0\doc
cp -f icons\autobga.ico icons\bga-tool-16.png icons\bga-tool-32.png icons\bga-tool-64.png autobga-sources-v1.0\icons
zip -9 -r autobga-sources-v1.0.zip ./autobga-sources-v1.0
rm -rf autobga-sources-v1.0