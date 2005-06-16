import gtk
import os

class NewProject:
	def __init__( self ):
		# Window
		self.win = gtk.Window()
		self.win.set_title( "New Project" )
		self.win.set_default_size( 350 , 400 )
		self.win.connect( "delete-event" , self.win_delete )

		# Main Box
		self.box = gtk.VBox()
		self.box.set_spacing( 5 )
		self.box.set_border_width( 10 )
		self.win.add( self.box )

		# Info frame
		self.iframe = gtk.Frame()
		self.iframe.set_shadow_type( gtk.SHADOW_ETCHED_IN )
		self.box.pack_start( self.iframe , False , True )

		# Info label
		self.ilabel = gtk.Label()
		self.ilabel.set_markup( "<b>Info</b>" )
		self.iframe.set_label_widget( self.ilabel )

		# Info table
		self.itable = gtk.Table( 2 , 2 )
		self.itable.set_row_spacings( 5 )
		self.itable.set_col_spacings( 5 )
		self.itable.set_border_width( 5 )
		self.iframe.add( self.itable )

		# Info Name label
		self.inlabel = gtk.Label( "Name:")
		self.inlabel.set_alignment( 0,0.5 )
		self.itable.attach( self.inlabel , 0,1,0,1 , gtk.FILL , gtk.FILL )

		# Info Name entry
		self.inentry = gtk.Entry()
		self.itable.attach( self.inentry , 1,2,0,1 , gtk.FILL|gtk.EXPAND , gtk.FILL )

		# Info Location label
		self.illabel = gtk.Label( "Location:" )
		self.illabel.set_alignment( 0,0.5 )
		self.itable.attach( self.illabel , 0,1,1,2 , gtk.FILL , gtk.FILL )

		# Info Location filechooserbutton
		self.ilfcb = gtk.FileChooserButton( "Project Location" )
		self.ilfcb.set_action( gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER )
		self.itable.attach( self.ilfcb , 1,2,1,2 , gtk.FILL|gtk.EXPAND , gtk.FILL )



		# TODO: Add Project type here




		# Commands frame
		self.cframe = gtk.Frame()
		self.cframe.set_shadow_type( gtk.SHADOW_ETCHED_IN )
		self.box.pack_start( self.cframe , False , True )

		# Commands label
		self.clabel = gtk.Label()
		self.clabel.set_markup( "<b>Commands</b>" )
		self.cframe.set_label_widget( self.clabel )

		# Commands table
		self.ctable = gtk.Table( 2,2 )
		self.ctable.set_border_width( 5 )
		self.ctable.set_row_spacings( 5 )
		self.ctable.set_col_spacings( 5 )
		self.cframe.add( self.ctable )

		# Commands Build label
		self.cblabel = gtk.Label( "Build:" )
		self.cblabel.set_alignment( 0,0.5 )
		self.ctable.attach( self.cblabel , 0,1,0,1 , gtk.FILL , gtk.FILL )

		# Commands Build entry
		self.cbentry = gtk.Entry()
		self.ctable.attach( self.cbentry , 1,2,0,1 , gtk.FILL|gtk.EXPAND , gtk.FILL )

		# Commands Execute label
		self.celabel = gtk.Label( "Execute:" )
		self.celabel.set_alignment( 0,0.5 )
		self.ctable.attach( self.celabel , 0,1,1,2 , gtk.FILL , gtk.FILL )

		# Commands Execute entry
		self.ceentry = gtk.Entry()
		self.ctable.attach( self.ceentry , 1,2,1,2 , gtk.FILL|gtk.EXPAND , gtk.FILL )



		# ButtonBox
		self.bbox = gtk.HButtonBox()
		self.bbox.set_spacing( 5 )
		self.bbox.set_layout( gtk.BUTTONBOX_END )
		self.box.pack_end( self.bbox , False , True )

		# Cancel
		self.cancel = gtk.Button( "Cancel" , gtk.STOCK_CANCEL )
		self.cancel.connect( "clicked" , self.cancel_clicked )
		self.bbox.pack_start( self.cancel )

		# OK
		self.ok = gtk.Button( "OK" , gtk.STOCK_OK )
		self.ok.connect( "clicked" , self.ok_clicked )
		self.bbox.pack_start( self.ok )

		# ButtonBox Separator
		self.bsep = gtk.HSeparator()
		self.box.pack_end( self.bsep , False , True )

		# Show all widgets
		self.win.show_all()

		# Set default response
		self.response = None

	def ok_clicked( self , *stuff ):
		name = self.inentry.get_text()
		if not name.endswith( ".mide" ): name += ".mide"
		location = self.ilfcb.get_filename()
		self.response = os.path.join( location , name )
		self._return()

	def cancel_clicked( self , *stuff ):
		self._return()

	def run( self ):
		gtk.main()
		return self.response

	def _return( self ):
		gtk.main_quit()

	def win_delete( self , *stuff ):
		self._return()




class MainWindow:
	def __init__( self , fn ):
		# Window
		self.win = gtk.Window()
		self.win.set_title( "mIDE: " + os.path.basename( fn ) )
		self.win.set_default_size( 200 , 400 )
		self.win.connect( "delete-event" , self.win_delete )

		# Box
		self.box = gtk.VBox()
		self.win.add( self.box )

		# Menu bar
		self.mbar = gtk.MenuBar()
		self.box.pack_start( self.mbar , False , True )

		# Menu File item
		self.mfitem = gtk.MenuItem( "File" )
		self.mbar.append( self.mfitem )

		# Toolbar
		self.tbar = gtk.Toolbar()
		#self.tbar.set_orientation( gtk.ORIENTATION_HORIZONTAL )
		#self.tbar.set_style( gtk.TOOLBAR_BOTH )
		self.box.pack_start( self.tbar , False , True )

		# Toolbar Build
		self.tbuild_image = gtk.image_new_from_stock( gtk.STOCK_CONVERT , gtk.ICON_SIZE_LARGE_TOOLBAR )
		self.tbuild = self.tbar.append_item(
				"Build",
				"Build Project",
				"Build Project",
				self.tbuild_image,
				self.tbuild_clicked )

		# Toolbar Execute
		self.texec_image = gtk.image_new_from_stock( gtk.STOCK_EXECUTE , gtk.ICON_SIZE_LARGE_TOOLBAR )
		self.texec = self.tbar.append_item(
				"Execute",
				"Execute Project",
				"Execute Project",
				self.texec_image,
				self.texec_clicked )





		# Show all widgets
		self.win.show_all()

	def texec_clicked( self , *stuff ):
		pass

	def tbuild_clicked( self , *stuff ):
		pass

	def run( self ):
		gtk.main()

	def win_delete( self , *stuff ):
		gtk.main_quit()
