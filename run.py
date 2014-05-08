from genCmdWrapper_win import *

xml_cmds = init_xmlCmd_rev1( 'cmds.xml',verbose = True )

commands = []
for cmd in xml_cmds.getCmds():
    commands.append( commandWrapper( cmd ) )


if __name__ == '__main__':
    app = QtGui.QApplication( sys.argv )
    dialog = Dialog( commands = commands )
    sys.exit( dialog.exec_() )