import sys
if "py2exe" in sys.argv:
	import py2exe
	from distutils.core import setup

	setup( name="mIDE" , version="0.1" , packages=["mIDE"] , windows=["mide.py"] )
else:
	from distutils.core import setup

	setup(
			name="mIDE",
			version="0.1",
			scripts=["mide.py"],
			packages=["mIDE"],
			)
