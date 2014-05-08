from PyQt4 import QtCore,QtGui
import sys


class cmdView( QtGui.QDialog ):
    def __init__( self,parent = None,fullCmdCommand = [""] ):
        super( cmdView,self ).__init__( parent )
        print "from window",fullCmdCommand
        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel
        layout_root = QtGui.QVBoxLayout()
        textQPlainTextEdit = QtGui.QPlainTextEdit()
        for cmd in fullCmdCommand:
            textQPlainTextEdit.insertPlainText( str( cmd + "\n" ) )

        layout_root.addWidget( textQPlainTextEdit )
        self.setLayout( layout_root )
        self.setWindowTitle( self.tr( "fileListView" ) )
        self.resize( 750,400 )

class fileListView( QtGui.QDialog ):
    def __init__( self,parent = None,inputDirectory = "c:\\notSet\\",outputDirectory = "c:\\notSet\\",fileListInput = ["file1","file2","file3","file4"],fileListOutput = ["fileOut1","file2Out","file3Out","file4Out"] ):
        super( fileListView,self ).__init__( parent )
        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel
        layout = QtGui.QGridLayout()
        layout.setColumnStretch( 0,0 )
        layout.setColumnMinimumWidth( 25,25 )
        self.fileListQListViewInput = QtGui.QListWidget ()
        self.fileListQListViewOutput = QtGui.QListWidget ()
        self.inputDirectoryQLabel = QtGui.QLabel ( str( inputDirectory ) )
        self.outputDirectoryQLabel = QtGui.QLabel ( str( outputDirectory ) )
        for item in fileListInput:
            self.fileListQListViewInput.addItems( [item] )
        for item in fileListOutput:
            self.fileListQListViewOutput.addItems( [item] )
        layout.addWidget ( QtGui.QLabel( "INPUT DIRECTORY" ),0,0 )
        layout.addWidget ( QtGui.QLabel( "OUPUT DIRECTORY" ),0,1 )
        layout.addWidget ( self.inputDirectoryQLabel,1,0 )
        layout.addWidget ( self.outputDirectoryQLabel,1,1 )
        layout.addWidget ( self.fileListQListViewInput,2,0 )
        layout.addWidget ( self.fileListQListViewOutput,2,1 )
        self.setLayout( layout )
        self.setWindowTitle( self.tr( "fileListView" ) )


class float3Input( QtGui.QDialog ):
    def __init__( self,parent = None,x = 0.0,y = 0.0,z = 0.0,decimals = 2 ):
        super( float3Input,self ).__init__( parent )
        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel
        layout = QtGui.QGridLayout()
        layout.setColumnStretch( 0,0 )
        layout.setColumnMinimumWidth( 25,25 )


        self.floatSpinBoxX = QtGui.QDoubleSpinBox()
        self.floatSpinBoxY = QtGui.QDoubleSpinBox()
        self.floatSpinBoxZ = QtGui.QDoubleSpinBox()
        self.floatSpinBoxX.setDecimals( decimals )
        self.floatSpinBoxY.setDecimals( decimals )
        self.floatSpinBoxZ.setDecimals( decimals )
        self.floatSpinBoxX.setValue( x )
        self.floatSpinBoxY.setValue( y )
        self.floatSpinBoxZ.setValue( z )

        self.labelFloatX = QtGui.QLabel( self.tr( "X" ) )
        self.labelFloatY = QtGui.QLabel( self.tr( "Y" ) )
        self.labelFloatZ = QtGui.QLabel( self.tr( "Z" ) )

        layout.addWidget ( self.labelFloatX,0,0 )
        layout.addWidget ( self.floatSpinBoxX,0,1 )
        layout.addWidget ( self.labelFloatY,0,2 )
        layout.addWidget ( self.floatSpinBoxY,0,3 )
        layout.addWidget ( self.labelFloatZ,0,4 )
        layout.addWidget ( self.floatSpinBoxZ,0,5 )

        self.buttonBox = QtGui.QPushButton( self.tr( "ok" ) )
        self.buttonBox.setObjectName( "buttonBox" )
        self.buttonBox.clicked.connect( self.accept )

        layout.addWidget ( self.buttonBox,0,6 )

        self.setLayout( layout )
        self.setWindowTitle( self.tr( "set3FloatDialog" ) )

    def exec_( self ):
        QtGui.QDialog.exec_( self )
        return [self.floatSpinBoxX.value(),self.floatSpinBoxY.value(),self.floatSpinBoxZ.value()]


class setnFloatInput( QtGui.QDialog ):
    def __init__( self,parent = None,n=8,decimals=5,titles=None ):
        """
        get n floats values from user, takes as arguments
        n numbers of floats to ask, decimals in floats, and titles[] to name the spinboxes in the
        interface
        if titles not received or if len(titles) does not equal n, default names are used
        """
        super( setnFloatInput,self ).__init__( parent )
        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel
        layout = QtGui.QGridLayout()
        layout.setColumnStretch( 0,0 )
        layout.setColumnMinimumWidth( 25,25 )

        self.floatSpinBox=[]
        self.floatLabel=[]
        bla=QtGui.QLabel()
        for value in range(0,n):
            self.floatSpinBox.append(QtGui.QDoubleSpinBox())
            self.floatSpinBox[value].setDecimals( decimals )
            self.floatSpinBox[value].setValue( 0 )
            self.floatLabel.append(QtGui.QLabel())
            if not titles == None:
                if len(titles)== n:
                    self.floatLabel[value].setText( self.tr( titles[value] ) )
            else:self.floatLabel[value].setText( self.tr( "Float" ) )
            layout.addWidget ( self.floatLabel[value],0,value )
            layout.addWidget (  self.floatSpinBox[value],1,value )

        self.buttonBox = QtGui.QPushButton( self.tr( "ok" ) )
        self.buttonBox.setObjectName( "buttonBox" )
        self.buttonBox.clicked.connect( self.accept )

        layout.addWidget ( self.buttonBox,1,n+1 )

        self.setLayout( layout )
        self.setWindowTitle( self.tr( "setnFloatDialog" ) )

    def exec_( self ):
        inputValues=[]
        for spinBox in self.floatSpinBox:
             inputValues.append(spinBox.value())
        print inputValues

app = QtGui.QApplication( sys.argv )
dialog = setnFloatInput(n=4,decimals=6, titles=["floatA","floatB","floatC","floatD","floatE","ultimo"])
sys.exit(dialog.exec_())


