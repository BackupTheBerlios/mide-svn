import gtk

class Store:
	def __init__( self ):
		self.view = None
		self.menu = None

	def new_project( self , name ):
		self.name = name
		if self.view: self.view.new_project( name )
		if self.menu: self.menu.new_project( )

class View( gtk.ScrolledWindow ):
	def __init__( self , store ):
		gtk.ScrolledWindow.__init__( self )
		self.set_policy( gtk.POLICY_AUTOMATIC , gtk.POLICY_AUTOMATIC )
		self.set_shadow_type( gtk.SHADOW_IN )

		self.store = store
		store.view = self

		# TreeView
		tv = self.tv = gtk.TreeView()
		tv.set_headers_visible( False )
		tv.connect( "button-press-event" , self.on_button_press )
		self.add( tv )

		# TreeModel
		model = self.model = gtk.TreeStore( gtk.gdk.Pixbuf , str )
		tv.set_model( model )

		# Pixbuf Column
		col = self.col = gtk.TreeViewColumn( "Name" )
		rend = gtk.CellRendererPixbuf()
		col.pack_start( rend , False )
		col.set_attributes( rend , pixbuf=0 )
		# Name Column
		rend = gtk.CellRendererText()
		col.pack_start( rend , True )
		col.set_attributes( rend , text=1 )
		tv.append_column( col )

		# Right-click menu
		popup = self.popup = gtk.Menu()
		item = gtk.MenuItem( "Add Folder" )
		popup.append( item )
		item = gtk.MenuItem( "Add File" )
		popup.append( item )
		popup.show_all()

		# Disable us
		self.set_sensitive( False )

	def new_project( self , name ):
		self.set_sensitive( True )
		self.tv.set_sensitive( True )
		model = self.model
		model.clear()
		i = model.append( None )
		model.set( i , 0 , self.tv.render_icon( gtk.STOCK_DIRECTORY , gtk.ICON_SIZE_MENU ) , 1 , name )
		self.tv.expand_all()

	def on_button_press( self , treeview , event ):
		# Show Right-click menu: self.popup
		if event.button == 3:
			x = int(event.x)
			y = int(event.y)
			time = event.time
			pthinfo = treeview.get_path_at_pos(x, y)
			if pthinfo != None:
				path, col, cellx, celly = pthinfo
				treeview.grab_focus()
				treeview.set_cursor( path, col, 0)
				self.popup.popup( None, None, None, event.button, time)

class Menu( gtk.MenuItem ):
	def __init__( self , store ):
		gtk.MenuItem.__init__( self , "Project" )

		# Project Store
		self.store = store
		store.menu = self

		# Menu
		menu = self.menu = gtk.Menu()
		self.set_submenu( menu )

		# New
		item = gtk.ImageMenuItem( gtk.STOCK_NEW )
		item.connect( "activate" , self.on_new_activated )
		menu.append( item )
		# Open
		item = gtk.ImageMenuItem( gtk.STOCK_OPEN )
		menu.append( item )
		# Save
		save = self.save = gtk.ImageMenuItem( gtk.STOCK_SAVE )
		save.set_sensitive( False )
		menu.append( save )
		# Save As
		saveas = self.saveas = gtk.ImageMenuItem( gtk.STOCK_SAVE_AS )
		saveas.set_sensitive( False )
		menu.append( saveas )

	def on_new_activated( self , widget , **data ):
		npw = self.npw = NewProjectWindow( None )
		npw.show()
		npw.connect( "response" , self.on_npw_response )

	def on_npw_response( self , widget , response ):
		name = self.npw.ne.get_text()
		location = self.npw.lf.get_filename()
		self.npw.hide()

		if response == gtk.RESPONSE_OK:
			self.store.new_project( name )

	def new_project( self ):
		self.save.set_sensitive( True )
		self.saveas.set_sensitive( True )



class NewProjectWindow( gtk.Dialog ):
	def __init__( self , parent ):
		gtk.Dialog.__init__( self , "New Project" , parent , gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT , ( gtk.STOCK_CANCEL , gtk.RESPONSE_CANCEL , gtk.STOCK_OK , gtk.RESPONSE_OK ) )


		# Table
		table = gtk.Table( 2 , 2 )
		table.set_row_spacings( 5 )
		table.set_col_spacings( 5 )
		table.set_border_width( 8 )
		self.vbox.pack_start( table )
		table.show()

		# Name Label
		l = gtk.Label( "Name:" )
		l.set_markup( "<b>Name:</b>" )
		l.set_alignment( 0 , 0.5 )
		table.attach( l , 0,1,0,1 , gtk.FILL , gtk.FILL )

		# Location Label
		l = gtk.Label( "Location:" )
		l.set_markup( "<b>Location:</b>" )
		l.set_alignment( 0 , 0.5 )
		table.attach( l , 0,1,1,2 , gtk.FILL , gtk.FILL )

		# Name Entry
		ne = self.ne = gtk.Entry()
		table.attach( ne , 1,2,0,1 , gtk.EXPAND|gtk.FILL , gtk.FILL )
		ne.show()

		# Location FileChooserButton
		lf = self.lf = gtk.FileChooserButton( "Project Location" )
		lf.set_action( gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER )
		table.attach( lf , 1,2,1,2 , gtk.EXPAND|gtk.FILL , gtk.FILL )
		lf.show()
	
		self.show_all()
