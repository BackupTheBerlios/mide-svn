import gtk
import os

import utils

class Store:
	def __init__( self ):
		self.view = None
		self.menu = None
		self.file = None
		self.project_files = []

	def clear( self ):
		self.project_files = []
		self.file = None

	def save( self ):
		if not self.file: return

		files = self.project_files[:]
		files.append( self.file )

		cp = utils.commonpath( files )

		files = self.project_files[:]

		fp = open( self.file , "w" )
		fp.write( "<mide version=\"1.0\">\n" )
		for file in files:
			fp.write( "<file>" + file[len(cp):] + "</file>\n" )
		fp.write( "</mide>\n" )
		fp.close()

	def add_file( self , fn ):
		self.project_files.append( fn )
		if self.view: self.view.file_added( fn )



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
		item.connect( "activate" , self.on_add_file )
		popup.append( item )
		popup.show_all()

		# Disable us
		#self.set_sensitive( False )

	def project_created( self ):
		self.set_sensitive( True )
		self.tv.set_sensitive( True )
		model = self.model
		model.clear()
		#i = model.append( None )
		#model.set( i , 0 , self.tv.render_icon( gtk.STOCK_DIRECTORY , gtk.ICON_SIZE_MENU ) , 1 , name )
		#self.tv.expand_all()

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
			else:
				self.popup.popup( None, None, None, event.button, time)

	def on_add_file( self , widget , *data ):
		fc = self.fc = gtk.FileChooserDialog( "Add File" , None , gtk.FILE_CHOOSER_ACTION_SAVE , ( gtk.STOCK_CANCEL , gtk.RESPONSE_CANCEL , gtk.STOCK_OK , gtk.RESPONSE_OK ) )
		fc.connect( "response" , self.on_add_file_response )
		fc.show()


	def on_add_file_response( self , widget , response ):
		fn = self.fc.get_filename()
		self.fc.hide()
		if response == gtk.RESPONSE_OK:
			self.store.add_file( fn )
		del self.fc

	def file_added( self , fn ):
		#print "File Added " + os.path.basename( fn )
		m = self.model
		i = m.append( None )
		m.set( i , 0 , self.tv.render_icon( gtk.STOCK_FILE , gtk.ICON_SIZE_MENU ) , 1 , os.path.basename( fn ) )
		

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
		save.connect( "activate" , self.on_save_activated )
		#save.set_sensitive( False )
		menu.append( save )
		# Save As
		saveas = self.saveas = gtk.ImageMenuItem( gtk.STOCK_SAVE_AS )
		saveas.connect( "activate" , self.on_save_as_activated )
		#saveas.set_sensitive( False )
		menu.append( saveas )

	def on_new_activated( self , widget , **data ):
		self.store.clear()

	def on_save_activated( self , widget , **data ):
		if self.store.file: self.store.save()
		else: self.on_save_as_activated( widget )

	def on_save_as_activated( self , widget , **data ):
		sfc = self.sfc = gtk.FileChooserDialog( "Save Project As" , None , gtk.FILE_CHOOSER_ACTION_SAVE , ( gtk.STOCK_CANCEL , gtk.RESPONSE_CANCEL , gtk.STOCK_OK , gtk.RESPONSE_OK ) )
		sfc.connect( "response" , self.on_sfc_response )
		sfc.show()


	def on_sfc_response( self , widget , response ):
		pf = self.sfc.get_filename()
		self.sfc.hide()
		if response == gtk.RESPONSE_OK:
			if not pf.endswith( ".mide" ): pf += ".mide"
			self.store.file = pf
			self.store.save()
		del self.sfc
