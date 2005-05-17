import os

def commonpath( list ):
	if len(list) < 2:
		return os.path.split( list[0] )[0] + "/"
		
	files = []
	for f in list:
		tmp = []
		if f.startswith( os.path.sep ): tmp.append( os.path.sep )
		tmp += f.split( os.path.sep )
		files.append( tmp )
	
	cp = ""
	finished = False
	while not finished:
		cur = files[0][0]
		for f in files:
			if not f[0] == cur: finished = True

		if not finished:
			tmp = []
			for f in files:
				tmp.append( f[1:] )
			files = tmp
			cp = os.path.join( cp , cur )

	if cp: cp += os.path.sep
	return cp
