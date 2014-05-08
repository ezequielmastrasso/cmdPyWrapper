import sys
from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import QTimeLine
from genCmdWrapper import *
from functools import partial
from extraDialogs import *


class ExtendedQLabel( QtGui.QLabel ):
    """
    A class of QLabel with added custom signal slots
    """
    def __init( self,parent ):
        QtGui.QLabel.__init__( self,parent )


    def mouseReleaseEvent( self,ev ):
        """
        Setups the mouseRelease signal
        Connect to this Using
        QtCore.SIGNAL( 'clicked()' ), func)
        """
        self.emit( QtCore.SIGNAL( 'clicked()' ) )


class FaderWidget( QtGui.QWidget ):
        """A dict that keeps keys in
        insertion order"""
        def __init__( self,old_widget,new_widget ):
            """A dict that keeps keys in insertion order"""
            QtGui.QWidget.__init__( self,new_widget )

            self.old_pixmap = QtGui.QPixmap( new_widget.size() )
            old_widget.render( self.old_pixmap )
            self.pixmap_opacity = 1.0
            self.timeline = QTimeLine()
            self.timeline.valueChanged.connect( self.animate )
            self.timeline.finished.connect( self.close )
            self.timeline.setDuration( 333 )
            self.timeline.start()

            self.resize( new_widget.size() )
            self.show()

        def paintEvent( self,event ):

            painter = QtGui.QPainter()
            painter.begin( self )
            painter.setOpacity( self.pixmap_opacity )
            painter.drawPixmap( 0,0,self.old_pixmap )
            painter.end()

        def animate( self,value ):

            self.pixmap_opacity = 1.0 - value
            self.repaint()

class StackedWidget( QtGui.QStackedWidget ):

        def __init__( self,parent = None ):
            """
            StackedWidget class to manage fade in/out when changing widget display
            """
            QtGui.QStackedWidget.__init__( self,parent )

        def setCurrentIndex( self,index ):
            self.fader_widget = FaderWidget( self.currentWidget(),self.widget( index ) )
            QtGui.QStackedWidget.setCurrentIndex( self,index )

        def setIndex1( self ):
            self.setCurrentIndex( 0 )

        def setIndex2( self ):
            self.setCurrentIndex( 1 )

        def setIndex3( self ):
            self.setCurrentIndex( 2 )

class Dialog( QtGui.QDialog ):

    def __init__( self,parent = None,commands = {} ):
        super( Dialog,self ).__init__( parent )
        self.commandList = []
        for command in commands:
            self.commandList.append( command.cmdName )
        self.commandSelected = self.commandList.index( self.setCommand() )
        self.command = commands[self.commandSelected]
        cmdName = self.command.cmdName
        self.resize( 1150,350 )

        #LAYOUTS!
        #top horizontal row
        layout_root = QtGui.QVBoxLayout()
        layout_top = QtGui.QHBoxLayout()
        layout_root.addLayout( layout_top )
        #first vertical column from the left, on horizontal top row
        #command Configs
        layout_top_vert1 = QtGui.QVBoxLayout()
        #Horizontal rows inside
        layout_top_vert1_boolAsString = QtGui.QHBoxLayout()
        layout_top_vert1_threads = QtGui.QHBoxLayout()
        layout_top_vert1_extension = QtGui.QHBoxLayout()
        layout_top_vert1_threads.setContentsMargins    ( 0,5,0,0 )
        layout_top_vert1_extension.setContentsMargins  ( 0,5,0,0 )
        layout_top.addLayout( layout_top_vert1 )

        #second vertical column from the left, on horizontal top row
        #file list view
        layout_top_Horizontal_vert2 = QtGui.QVBoxLayout()
        layout_top_Horizontal_vert2_Top = QtGui.QHBoxLayout()
        layout_top.addLayout( layout_top_Horizontal_vert2 )

        #middle layout, vertical to hold the 3 column options row

        self.layout_middle = QtGui.QVBoxLayout()
        layout_root.addLayout( self.layout_middle )


        #fileView
        self.excelWidget = QtGui.QTableWidget()
        self.excelWidget.setShowGrid( True )
        self.excelWidget.setColumnCount( 2 )
        self.excelWidget.setColumnWidth( 0,495 )
        self.excelWidget.setColumnWidth( 1,495 )
        self.excelWidget.setRowCount( 0 )
        self.excelWidget.verticalHeader().setDefaultSectionSize( 17 )
        self.excelWidget.setSortingEnabled( 1 )
        self.excelWidget.setHorizontalHeaderLabels( ["inputFiles","outputFiles"] )

        #CMD Config controls
        configButtonSize = 18
        if self.command.inputFile:
            #if self.command.multipleinputFiles:
            files_inputFilesButton = QtGui.QPushButton( self.tr( "Select Input Files" ) )
            files_inputFilesButton.clicked.connect( self.setOpenFileNames )
            files_inputFilesButton.setFixedHeight  ( configButtonSize )
        else:
            files_inputFilesButton = QtGui.QPushButton( self.tr( "Select output FileName" ) )
            files_inputFilesButton.setFixedHeight  ( configButtonSize )
            files_inputFilesButton.clicked.connect( self.setOutputFileName )

        files_outputDirectoryButton = QtGui.QPushButton( self.tr( "Select Output Directory" ) )
        files_previewCmdButton = QtGui.QPushButton( self.tr( "preview Commands" ) )
        files_saveScriptButton = QtGui.QPushButton( self.tr( "save Script" ) )
        files_scheduleCmdButton = QtGui.QPushButton( self.tr( "schedule Command" ) )
        uncheckAllButton = QtGui.QPushButton( self.tr( "uncheck all" ) )
        files_processButton = QtGui.QPushButton( self.tr( "START!" ) )



        files_outputDirectoryButton.setFixedHeight  ( configButtonSize )
        files_previewCmdButton.setFixedHeight  ( configButtonSize )
        files_saveScriptButton.setFixedHeight  ( configButtonSize )
        files_scheduleCmdButton.setFixedHeight  ( configButtonSize )
        files_processButton.setFixedHeight  ( 30 )

        files_threadsLabel = QtGui.QLabel( "threads" )
        files_threadsN = QtGui.QSpinBox()
        files_threadsN.setValue( 1 )

        files_extensionLabel = QtGui.QLabel( "fileExt" )
        files_extensionQComboBox = QtGui.QComboBox()
        files_extensionQComboBox.setFixedWidth( 50 )
        files_extensionQComboBox.setEditable( 1 )

        files_extensionQComboBox.addItems( [self.command.files_outputExtension] )

        #signaling
        files_processButton.clicked.connect( self.process )
        files_outputDirectoryButton.clicked.connect( self.setExistingDirectory )
        files_previewCmdButton.clicked.connect( self.reviewCmd )
        uncheckAllButton.clicked.connect( self.uncheckAll )

        #add stretchiness and stuff
        layout_top_vert1.setStretch( 1,1 )
        layout_top_vert1.setSpacing( 0 )
        layout_top_vert1.addWidget( files_inputFilesButton )
        layout_top_vert1.addWidget( files_outputDirectoryButton )
        layout_top_vert1.addWidget( files_previewCmdButton )
        layout_top_vert1.addWidget( uncheckAllButton )
        layout_top_vert1.addWidget( files_saveScriptButton )
        layout_top_vert1.addWidget( files_scheduleCmdButton )
        layout_top_vert1.addStretch( 1 )
        layout_top_vert1.addLayout( layout_top_vert1_boolAsString )
        layout_top_vert1_threads.addWidget( files_threadsLabel )
        layout_top_vert1_threads.addWidget( files_threadsN )
        layout_top_vert1_extension.addWidget( files_extensionLabel )
        layout_top_vert1_extension.addWidget( files_extensionQComboBox )
        layout_top_vert1.addLayout( layout_top_vert1_extension )
        layout_top_vert1.addStretch( 1 )

        layout_top_vert1.addLayout( layout_top_vert1_threads )
        layout_top_vert1.addStretch( 1 )
        layout_top_vert1.addStretch( 1 )
        layout_top_vert1.addWidget( files_processButton )

        self.boolAsStringQCheckBox = QtGui.QCheckBox()
        boolAsStringQLabel = QtGui.QLabel( "bool as strings" )

        self.boolAsStringQCheckBox.toggled.connect( self.setBoolAsString )

        layout_top_vert1_boolAsString.addWidget( boolAsStringQLabel )
        layout_top_vert1_boolAsString.addWidget( self.boolAsStringQCheckBox )


        layout_top_Horizontal_vert2.addLayout( layout_top_Horizontal_vert2_Top )

        viewFileListButton = QtGui.QPushButton( "viewFileList" )
        viewMiscButton = QtGui.QPushButton( "viewMisc" )
        workersStdoutButton = QtGui.QPushButton( "workersStdout" )

        layout_top_Horizontal_vert2_Top.addWidget( viewFileListButton )
        layout_top_Horizontal_vert2_Top.addWidget( viewMiscButton )
        layout_top_Horizontal_vert2_Top.addWidget( workersStdoutButton )

        self.viewMiscButtonQPlainTextEdit = QtGui.QPlainTextEdit()
        self.progressBar = QtGui.QProgressBar()
        self.progressBar.setValue( 0 )
        self.progressBar.valueChanged.connect( self.processFinishedWindow )

        self.stack = StackedWidget()
        layout_top_Horizontal_vert2.addWidget( self.stack )

        self.columnNQSlider = QtGui.QSlider()
        self.columnNQSlider.setOrientation( 0x1 )
        self.columnNQSlider.setMinimum( 3 )
        self.columnNQSlider.setMaximum( 12 )
        self.columnNQSlider.setValue( 8 )
        self.columnNQSlider.setTickInterval( 1 )
        self.columnNQSlider.setTickPosition( 2 )

        self.columnNQSlider.valueChanged.connect( self.rearrangeOptions )

        layout_top_Horizontal_vert2.addWidget( self.columnNQSlider )

        self.stack.addWidget( self.excelWidget )
        self.stack.addWidget( self.viewMiscButtonQPlainTextEdit )
        self.stack.addWidget( self.progressBar )

        viewFileListButton.clicked.connect( self.stack.setIndex1 )
        viewMiscButton.clicked.connect( self.reviewCmd )
        workersStdoutButton.clicked.connect( self.stack.setIndex3 )

        #CMD! OPTIONS
        self.optionsNames = self.command.options.keys()
        self.optionNumber = len( self.command.options.keys() )
        maxColumn = 8
        if self.optionNumber % maxColumn == 0:
            rowNumber = self.optionNumber / maxColumn
        else:
            rowNumber = ( self.optionNumber / maxColumn ) + 1
        i = 0
        self.optionQGroupBox = []
        optionCharQLabel=[]
        optionQLabel = []
        self.layout_middle_Hor = []
        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel
        for row in range( 0,rowNumber ):
            self.layout_middle_Hor.append( QtGui.QHBoxLayout() )
            self.layout_middle.addLayout( self.layout_middle_Hor[row] )
            for column in range( 0,maxColumn ):
                currentOptionName = self.optionsNames[i]
                self.optionQGroupBox.append( QtGui.QGroupBox() )

                optionCharQLabel.append( ExtendedQLabel() )
                optionQLabel.append( ExtendedQLabel() )

                optionCharQLabel[i].setParent( self.optionQGroupBox[i] )
                optionCharQLabel[i].setParent( self.optionQGroupBox[i] )
                optionQLabel[i].setParent( self.optionQGroupBox[i] )

                self.optionQGroupBox[i].setTitle( currentOptionName )
                self.optionQGroupBox[i].setCheckable( 1 )
                self.optionQGroupBox[i].setChecked( self.command.options[currentOptionName].state )
                self.optionQGroupBox[i].setFixedHeight( 51 )
                #self.optionQGroupBox[i].setFlat(1)
                self.optionQGroupBox[i].setAlignment(0)


                optionCharQLabel[i].move( 8,25 )
                optionQLabel[i].move( 29,25 )

                #TODO:add - -- / as option prefixs
                optionCharQLabel[i].setText( str(self.command.options[currentOptionName].optionPrefix) )


                optionQLabel[i].setText( str( self.command.options[currentOptionName].param.value[0] ) )

                #optionQLabel[i].setFrameStyle( frameStyle )

                optionCharQLabel[i].setFixedWidth( 20 )
                optionQLabel[i].setFixedWidth( 90 )

                self.layout_middle_Hor[row].addWidget( self.optionQGroupBox[i] )

                #signals
                self.connectCheckbox( self.optionQGroupBox[i],self.optionsNames[i] )
                currentParamType = self.command.options[currentOptionName].paramTypeString
                #connects option QLabel to custom dialog for user input
                self.connectButton( currentParamType,
                                    optionQLabel[i],
                                    optionQLabel[i],
                                    i,
                                    currentOptionName )
                #connects option prefix QLabel to custom dialog for user input
                self.connectQLabelOptionChar( optionCharQLabel[i],
                                              i,
                                              currentOptionName )



                if i == self.optionNumber - 1:
                    break
                i += 1

        #bottom layout
        self.setLayout( layout_root )
        self.setWindowTitle( self.tr( cmdName ) )

    def setOutputFileName(self):
        """
        asks the user to select an item from a list, also editable for custom string parameters
        """
        items = QtCore.QStringList("")
        itemCurrentIndex = 0
        item,ok = QtGui.QInputDialog.getItem( self,
                self.tr( "QInputDialog.getItem()" ),
                self.tr( "fileName:" ),
                items,
                itemCurrentIndex,
                True )
        if ok and not item.isEmpty():
            #set the currentIndex based on the "string" passed
            self.command.files_outputFile=[str(item)]

    def connectQLabelOptionChar(self,optionCharQLabel,index,currentOptionName):
        self.connect ( optionCharQLabel,
                       QtCore.SIGNAL( 'clicked()' ),
                       partial( self.setOptionPrefix,
                                optionCharQLabel,
                                index,
                                currentOptionName
                                ) )
    def setOptionPrefix(self,nameQLabel,index,currentOptionName ):
        """
        asks the user to select an item from a list, also editable for custom string parameters
        """
        itemList = [self.command.options[currentOptionName].optionPrefix]
        items = QtCore.QStringList()
        itemCurrentIndex = 0
        for item in itemList:
            items << self.tr( str( item ) )
        item,ok = QtGui.QInputDialog.getItem( self,
                self.tr( "QInputDialog.getItem()" ),
                self.tr( "itemList:" ),
                items,
                itemCurrentIndex,
                True )
        if ok and not item.isEmpty():
            self.command.options[currentOptionName].optionPrefix=( str( item ) )
            nameQLabel.setText( self.tr( item ) )


    def rearrangeOptions( self ):
        """rearrange the middle middle_hotLayout
        depending on the column n"""
        maxColumn = self.columnNQSlider.value()
        if self.optionNumber % maxColumn == 0:
            rowNumber = self.optionNumber / maxColumn
        else:
            rowNumber = ( self.optionNumber / maxColumn ) + 1
        i = 0
        for rowLayout in self.layout_middle_Hor:
            rowLayout.setParent( None )
            del rowLayout
        self.layout_middle_Hor = []
        for QGroupBox in self.optionQGroupBox:
            QGroupBox.setParent( None )
        for row in range( 0,rowNumber ):
            self.layout_middle_Hor.append( QtGui.QHBoxLayout() )
            self.layout_middle.addLayout( self.layout_middle_Hor[row] )
            for column in range( 0,maxColumn ):
                    self.layout_middle_Hor[row].addWidget( self.optionQGroupBox[i] )
                    if i == self.optionNumber - 1:
                        break
                    i += 1
        self.resize( 1150,250 )


    def setBoolAsString( self,boolAsStringQCheckBox ):
        """Sets the bool value to pass the boolean args to the cmd as a
        string value or equivalent value."""
        newValue = self.boolAsStringQCheckBox.isChecked()
        for option in self.command.options.keys():
            if self.command.options[option].paramTypeString == "Boolean":
                self.command.options[option].param.boolAsString = newValue

    def updateFileTable( self ):
        """updates the interface file input output spreadsheet"""
        n = len( self.command.files_inputFiles )
        self.excelWidget.setRowCount( 0 )
        self.excelWidget.setRowCount( n + 1 )
        if self.command.inputFile:
            self.excelWidget.setItem( 0,0,QtGui.QTableWidgetItem( self.command.files_inputDirectory ) )
        else:
            self.excelWidget.setItem( 0,0,QtGui.QTableWidgetItem( "no input files" ) )
        self.excelWidget.setItem( 0,1,QtGui.QTableWidgetItem( self.command.files_outputDirectory ) )
#        for i in range( 0,n ):
#            self.excelWidget.setItem( 0,2 + ( i * 2 ),QtGui.QTableWidgetItem( self.command.files_inputFiles[i] ) )
##            if not self.command.multipleOutputFiles:
#            self.excelWidget.setItem( 0,3 + ( i * 2 ),QtGui.QTableWidgetItem( self.command.files_outputFile[0] ) )
#            #else:self.excelWidget.setItem( 0,3 + ( i * 2 ),QtGui.QTableWidgetItem( self.command.files_outputFile[i] ) )


    def reviewCmd ( self ):
        """sets the top middle stacked widget value to view mode"""
        self.command.debug()
        self.viewMiscButtonQPlainTextEdit.clear()
        for cmd in self.command.fullCmdCommand:
            for arg in cmd:
                self.viewMiscButtonQPlainTextEdit.insertPlainText(str(" " + str(arg)))
            self.viewMiscButtonQPlainTextEdit.insertPlainText( str( "\n" ) )
        self.stack.setIndex2()

    def process( self ):
        """updates the commands to run and send the commands[] to sleepProgress to
        run as a background pr"""
        print "Running!"
        self.command.debug()
        self.progressBar.setValue( 0 )
        self.stack.setIndex3()
        self.thread = SleepProgress( cmdLines = self.command.fullCmdCommand )
        self.thread.partDone.connect( self.updatePBar )
        #self.thread.procDone.connect( self.fin )

        self.thread.start()

    def processFinishedWindow( self ):
        """
        if progressBarValue is 100 pop up window saying is done
        """
        if self.progressBar.value() == 100:
            QtGui.QMessageBox.about( None,"Notice","done!" )

    def updatePBar( self,val ):
        """
        updates the progressBar value
        """
        self.progressBar.setValue( val )

    def uncheckAll( self ):
        """
        sets False to all argument options state on optionObjects
        """
        for checkBox in self.optionQGroupBox:
            checkBox.setChecked( 0 )

    def setCommand( self ):
        """
        lists the commands found in the xml and makes the user pick one
        to work with
        """
        itemList = self.commandList
        items = QtCore.QStringList()
        for item in itemList:
            items << self.tr( str( item ) )
        item,ok = QtGui.QInputDialog.getItem( self,
                self.tr( "QInputDialog.getItem()" ),
                self.tr( "itemList:" ),
                items,
                0,
                True )
        if ok and not item.isEmpty():
            #set the currentIndex based on the "string" passed
            return item

    def setExistingDirectory( self ):
        """
        asks the user for a directory
        """
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory( self,
                self.tr( "QFileDialog.getExistingDirectory()" ),
                "",options )
        if not directory.isEmpty():
            self.command.files_outputDirectory = directory + "\\"
            self.updateFileTable()

    def setOpenFileName( self ):
        """
        asks the user for a file
        """
        options = QtGui.QFileDialog.Options()
        if True:
            options |= QtGui.QFileDialog.DontUseNativeDialog
        selectedFilter = QtCore.QString()
        fileName = QtGui.QFileDialog.getOpenFileName( self,
                self.tr( "QFileDialog.getOpenFileName()" ),
                "",
                self.tr( "All Files (*)" ),selectedFilter,
                options )
        if not fileName.isEmpty():
            self.command.files_inputFiles = [ str( fileName ) ]
            self.command.setInputFilesFromAbsolutePaths( [ str( fileName ) ] )
            self.updateFileTable()

    def setOpenFileNames( self ):
        """
        asks the user for files
        """
        options = QtGui.QFileDialog.Options()
        if True:
            options |= QtGui.QFileDialog.DontUseNativeDialog
        selectedFilter = QtCore.QString()
        fileNames = QtGui.QFileDialog.getOpenFileNames( self,
                self.tr( "QFileDialog.getOpenFileNames()" ),"",
                self.tr( "All Files (*)" ),selectedFilter,
                options )
        if fileNames.count():
            files = []
            for index in range( 0,fileNames.count() ):
                files.append( str( fileNames[index] ) )
            self.command.files_inputFiles = files
            self.command.setInputFilesFromAbsolutePaths( files )
#            self.updateFileTable()


    def setItem( self,nameQLabel,index,currentOptionName ):
        """
        asks the user to select an item from a list, also editable for custom string parameters
        """
        itemList = self.command.options[currentOptionName].param.list
        items = QtCore.QStringList()
        itemCurrentIndex = self.command.options[currentOptionName].param.index
        for item in itemList:
            items << self.tr( str( item ) )
        item,ok = QtGui.QInputDialog.getItem( self,
                self.tr( "QInputDialog.getItem()" ),
                self.tr( "itemList:" ),
                items,
                itemCurrentIndex,
                True )
        if ok and not item.isEmpty():
            #set the currentIndex based on the "string" passed
            self.command.options[currentOptionName].param.set_valueFromString( str( item ) )
            nameQLabel.setText( self.tr( item ) )

    def connectButton( self,currentParamType,button,nameQLabel,index,currentOptionName ):
        """
        connects the interface control passed as an argument to the corresponding askUser dialog data Type
        """
        if currentParamType == "float":
            self.connect          ( nameQLabel,
                                   QtCore.SIGNAL( 'clicked()' ),
                                   partial( self.setfloat,
                                            nameQLabel,
                                            index,
                                            #getLabelText QString object and cast to int
                                            currentOptionName
                                            ) )
        if currentParamType == "Integer":
            self.connect          ( nameQLabel,
                                   QtCore.SIGNAL( 'clicked()' ),
                                   partial( self.setInteger,
                                            nameQLabel,
                                            index,
                                            #getLabelText QString object and cast to int
                                            currentOptionName
                                            ) )
        if currentParamType == "fixedString" or currentParamType == "string":
            self.connect          ( nameQLabel,
                                   QtCore.SIGNAL( 'clicked()' ),
                                   partial( self.setItem,
                                            nameQLabel,
                                            index,
                                            #getLabelText QString object and cast to int
                                            currentOptionName
                                            ) )
        if currentParamType == "Boolean":
            self.connect          ( nameQLabel,
                                   QtCore.SIGNAL( 'clicked()' ),
                                   partial( self.setItem,
                                            nameQLabel,
                                            index,
                                            #getLabelText QString object and cast to int
                                            currentOptionName
                                            ) )
        if currentParamType == "float3":
            self.connect          ( nameQLabel,
                                   QtCore.SIGNAL( 'clicked()' ),
                                   partial( self.setfloat3,
                                            nameQLabel,
                                            #getLabelText QString object and cast to int
                                            currentOptionName
                                            ) )

    def setfloat3( self,nameQLabel,currentOptionName ):
        """
        asks the user for 3 floats
        """
        x = float( self.command.options[currentOptionName].param.value[0][0] )
        y = float( self.command.options[currentOptionName].param.value[0][1] )
        z = float( self.command.options[currentOptionName].param.value[0][2] )
        dialog = float3Input( x = x,y = y,z = z,decimals = 8 )
        returnValue = dialog.exec_()
        self.command.options[currentOptionName].param.set_value( returnValue )
        nameQLabel.setText( self.tr( str( returnValue ) ) )

    def connectCheckbox( self,checkbox,currentOptionName ):
        """
        connects the toggled emitted signal from a checkbox to the change state parameter function
        """

        checkbox.toggled.connect( partial( self.changeParamActiveState,
                                        checkbox,
                                        currentOptionName
                                        ) )

    def changeParamActiveState( self,checkbox,currentOptionName ):
        """
        changes the active state of an option object passed as the argument to the corresponding
        interface checkbox object
        """
        if checkbox.isChecked() == True:
            value = True
        else: value = False
        #setsActiveState
        self.command.options[currentOptionName].state = value



    def setfloat( self,nameQLabel,index,currentOptionName ):
        """
        asks the user for a float value
        """
        #cast the activeParamValue to float
        value = self.command.options[currentOptionName].param.value[0]
        d,ok = QtGui.QInputDialog.getDouble( self,
                                             self.tr( "QInputDialog.getDouble()" ),self.tr( "Float:" ),
                                             value,
                                             - 650,650,15 )
        if ok:
            #update interface label
            nameQLabel.setText( self.tr( "%5" ).arg( d ) )
            #sets the activeParam[0] to value in input
            self.command.options[currentOptionName].param.set_value( d )



    def setInteger( self,nameQLabel,index,currentOptionName ):
        """
        asks the user for a integer
        """
        value = self.command.options[currentOptionName].param.value[0]
        i,ok = QtGui.QInputDialog.getInteger( self,
                                              self.tr( "QInputDialog.getInteger()" ),self.tr( "Integer:" ),
                                              value,
                                              - 65000,65000,1 )
        if ok:
            #update interface label
            nameQLabel.setText( self.tr( "%1" ).arg( i ) )
            #sets the activeParam[0] to value in input
            self.command.options[currentOptionName].param.set_value( i )

xml_cmds = init_xmlCmd_rev1( 'cmds.xml',verbose = False )

commands = []
for cmd in xml_cmds.getCmds():
    commands.append( commandWrapper( cmd ) )

