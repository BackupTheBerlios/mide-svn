import gtk

import project

class MainWindow:
	def __init__( self ):
		# Window
		win = self.win = gtk.Window()
		win.set_title( "mIDE" )
		win.set_size_request( 600,400 )

		# Main box
		box = self.box = gtk.VBox( False )
		win.add( box )

		# Menu bar
		menubar = self.menubar = gtk.MenuBar()
		box.pack_start( menubar , False , True )

		# Pane
		pane = self.pane = gtk.HPaned()
		box.pack_start( pane , True , True )

		# Project Store
		ps = self.ps = project.Store()

		# Project View
		pv = self.pv = project.View( ps )
		pane.add( pv )

		# Project Menu
		pm = self.pm = project.Menu( ps )
		menubar.append( pm )


		# Placeholder
		ph = gtk.Label( "Placeholder for a Editor" )
		pane.add2( ph )

		win.show_all()


mw = MainWindow()
gtk.main()
		
