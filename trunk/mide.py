import gtk

import project

class MainWindow:
	def __init__( self ):
		# Window
		win = self.win = gtk.Window()
		win.set_title( "mIDE" )
		win.set_size_request( 200 , 400 )
		win.connect( "delete-event" , self.on_win_delete )

		# Main box
		box = self.box = gtk.VBox( False )
		win.add( box )

		# Menu bar
		menubar = self.menubar = gtk.MenuBar()
		box.pack_start( menubar , False , True )

		# Project Store
		ps = self.ps = project.Store()

		# Project View
		pv = self.pv = project.View( ps )
		box.pack_start( pv , True , True )

		# Project Menu
		pm = self.pm = project.Menu( ps )
		menubar.append( pm )

		win.show_all()

	def on_win_delete( self , widget , *data ):
		gtk.main_quit()

mw = MainWindow()
gtk.main()
		
