#!python
import mIDE
import sys
import os

args = sys.argv

pf = None
if len( args ) > 1:
	if args[1].endswith(".mide"):
		pf = os.path.abspath(args[1])
else:
	np = mIDE.NewProject()
	pf = np.run()
if pf:
	mw = mIDE.MainWindow( pf )
	mw.run()
