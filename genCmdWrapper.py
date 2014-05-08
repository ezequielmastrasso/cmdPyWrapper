
from odict import *
from genCmdWrapper_xml_rev1 import *
import os

from PyQt4 import QtCore,QtGui
import subprocess

class SleepProgress( QtCore.QThread ):
    procDone = QtCore.pyqtSignal( bool )
    partDone = QtCore.pyqtSignal( int )
    def __init__( self,cmdLines ):
        super( SleepProgress,self ).__init__( None )
        self.cmdLines = cmdLines

    def run( self ):
        print 'proc started'
        commandsN = len( self.cmdLines )
        self.partDone.emit( ( 100 / commandsN ) * .5 )
        pipeStr=""
        for i in range( 0,commandsN ):
            execute = subprocess.Popen( self.cmdLines[i],shell = True)# stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#            pipestdout=execute.communicate()
#            print "piping:",pipestdout
#            pipeTo = subprocess.Popen(["D:\\dev\\grep\\bin\\grep.exe", ("\""+pipestdout[0]+"\""), pipestdout])

            execute.wait()
            self.partDone.emit( ( 100 / commandsN ) * ( i + 1 ) )
            print "worker done:  ",( 100 / commandsN ) * ( i + 1 )
            self.partDone.emit ( ( 100 / commandsN ) * ( i + 1 ) )
        self.procDone.emit( True )
        print 'proc ended'

#--------------------------------------------------------------------------------------------#
#---------------------------------------OBJECTS-BEGING---------------------------------------#
class commandWrapper ( object ):
    def __init__( self,cmd ):
        """
        commandWrapper class
        Holds the command configuration and containts option objects with argument
        parameters and types
        =======================================================================
         ----------------------COMMAND-DICT-EXAMPLES--------------------------
        self.config = {
                         "inputFile"    :True,
                         "outputFile"   :True,
                         "cmdPath"      :"c:\programFiles\prman\bin"
                         }
        self.cmdOptionsSource = OrderedDict( [( 'example_Integer',[False,
                                                                        "Integer",
                                                                        0,
                                                                        [8]
                                                                        ], ),
                                             ( 'example_float',        [False,
                                                                        "float",
                                                                        0,
                                                                        [1.5]
                                                                        ] ),
                                             ( 'example_fixedStringList',[False,
                                                                        "fixedString",
                                                                        0,
                                                                        ["paramb1","paramb2","paramb3"]
                                                                        ] ),
                                             ( 'example_boolean',        [False,
                                                                        "Boolean",
                                                                        0,
                                                                        [True,False]
                                                                        ] ),
                                             ( 'example_3floatvector',    [False,
                                                                        "float3",
                                                                        0,
                                                                        [1.0,2.0,3.0]
                                                                        ] ),
                                             ( 'example_string',        [False,
                                                                        "string",
                                                                        0,
                                                                        ["customString"]
                                                                        ] ),
                                             ] )
        #=======================================================================
        #---------------------------------EXAMPLES-----------------------------#
        #=======================================================================
         self.cmdOptionsSource
         print cmd[cmd.keys()[0]]['cmdOptions']
         print self.cmdOptionsSource
         print cmd[cmd.keys()[0]]
         print self.cmdOptionsSource.keys()
         print cmd[cmd.keys()[0]]['cmdOptions'].keys()
        #=======================================================================
         for option in self.options.keys():
            print "cmdOptionName:           ", option
            print "    activeParamIndex:        ", self.options[option].param.index
            print "    paramList:               ", self.options[option].param.list
            print "        currentValue:            ", self.options[option].param.value

            self.options[option].set_index(1)                #boolean

            self.options[option].setValue( True )              #boolean
            self.options[option].setValue( 1 )                 #integer
           self.options[option].setValue( 1.0 )               #float
            self.options[option].setValue( [1.0,1.0,1.0] )     #3floatvector
            self.options[option].setValue( ["","","",...] )    #fixedStringList
            self.options[option].setValue( [""] )              #string
        #=======================================================================

        """
        cmdName = cmd.keys()[0]
        self.cmdName = cmd.keys()[0]
        self.configSource = cmd[cmdName]["cmdConfig"]
        self.inputFile = self.configSource["inputFile"]
        self.multipleinputFiles = self.configSource["multipleinputFiles"]
        self.outputFile = self.configSource["outputFile"]
        self.cmdFile = self.configSource["cmdFile"]
        self.cmdPath = self.configSource["cmdPath"]
        self.fullCmdCommand = ""


        self.files_inputFiles = [""]
        self.files_inputDirectory = ""
        self.files_outputDirectory = ( os.getenv( 'USERPROFILE' ) or os.getenv( 'HOME' ) ) + "/"
        self.files_prePosFix = [1,"_new"]
        self.files_outputFile = ["default"]
        self.files_outputExtension = self.configSource["outputFileExtension"]

        self.options = OrderedDict()

        self.cmdOptionsSource = cmd.values()[0]["cmdOptions"]
        self.createOptionsFromDict()


    def __str__( self ):
        """
        prints a pretty cmd structure to stdout and commands!
        """
        string=""
        stringChild=    "    |-----"
        stringLastChild="    `-----"
        string=string+self.cmdName+"\n"

        for optionName in self.cmdOptionsSource.keys():
            string=string+"\t"+optionName+"\n"

            string=string+"\t"+stringChild       + "state: " + str(self.cmdOptionsSource[optionName][0])+"\n"

            string=string+"\t"+stringChild       + "type: "+ str(self.cmdOptionsSource[optionName][1])+"\n"

            string=string+"\t"+stringChild   + "index: "+str(self.cmdOptionsSource[optionName][2])+"\n"

            if self.cmdOptionsSource[optionName][1] != "string":
                string=string+"\t"+stringChild   + "prefix: " + str(self.cmdOptionsSource[optionName][4])+"\n"

            else:
                string=string+"\t"+stringLastChild   + "prefix: " + str(self.cmdOptionsSource[optionName][4])+"\n"

            if self.cmdOptionsSource[optionName][1] != "string":
                string=string+"\t"+stringLastChild   + "options"+"\n"

                n=len(self.cmdOptionsSource[optionName][3])
                for item in range(0,n):
                    if item!=n-1:
                        string=string+"\t\t" + stringChild +str(self.cmdOptionsSource[optionName][3][item]) + "\t"+"\n"
                    else:
                        string=string+"\t\t" + stringLastChild +str(self.cmdOptionsSource[optionName][3][item]) + "\t"+"\n"


        return string


    def createOptionsFromDict(self):
        """
        See also __init__ for input dict structure
        #=======================================================================
         --------Parse incoming cmdOptionsSource dict and create objects-----------#
                self.cmdOptionsSource=OrderedDict([('example_string', [False,
                                                                    "string",
                                                                    0,
                                                                    ["customString"]
                                                                    ]),
                                                    ] )
        #=======================================================================
        """
        for option in self.cmdOptionsSource.keys():
            state = self.cmdOptionsSource[option][0]
            paramTypeString = self.cmdOptionsSource[option][1]
            index = self.cmdOptionsSource[option][2]
            list = self.cmdOptionsSource[option][3]
            prefix= self.cmdOptionsSource[option][4]
            #--------iterate and create commandOption(Objects)---------------------#
            self.options[option] = commandOption( paramTypeString,
                                                  state,
                                                  index,
                                                  list,
                                                  prefix )


    def setInputFilesFromAbsolutePaths( self,inputFiles ):
        """
        #=======================================================================
         if inputFile
            if    multipleInputFiles and multipleOutputFiles
                    command=cmd input1 output1
                    command+=cmd input2 output2
                    command+=cmd input3 output3
            elif  multipleInputFiles and not multipleOutputFiles
                    command=cmd input1 input2 input3 output1
            else
                  command=cmd output1
        #=======================================================================
        """
        self.files_inputFiles = []
        for fileAbsolutePath in inputFiles:
            fileName = os.path.split( fileAbsolutePath )[1]
            self.files_inputFiles.append( fileName )
        self.files_inputDirectory = os.path.split( inputFiles[0] )[0] + "/"
        self.files_outputFile = []
        if self.inputFile:
                for file in self.files_inputFiles:
                    fileName = os.path.splitext( file )[0]
                    self.files_outputFile.append( fileName + "." + self.files_outputExtension )

    def debug( self ):
            """
            #===================================================================
            1liners
                A

                B
                cmd --options input1 input2 input3
                C
                cmd --options output1
                D
                cmd --options input1 input2 input3 output1
            multipleLiners
                E
                cmd --options input1 output1

            #===================================================================
            if input and not multipleInput and not output
                cmd --options input1
                cmd --options input2
                cmd --options input3

            elif input and multiple input and no output
                cmd --options input1 input2 input3

            elif not input and output
                cmd --options output1

            elif input and multiple input and output
                cmd --options input1 input2 input3 output1

            elif input and output
                cmd --options input1 output1
                cmd --options input2 output2

            else
                warning, check your xml conf input and output options!!!

            #===================================================================
            """
            argumentCmd = self.cmdPath + "\\" + self.cmdFile
            arguments = []
            postArguments = []
            inputFiles = []
            outputFiles = []

            if self.files_inputDirectory!= None:
                if self.inputFile:
                    for file in self.files_inputFiles:
                        inputFiles.append( self.files_inputDirectory + file )
                    if self.outputFile:
                        for file in self.files_outputFile:
                            outputFiles.append( self.files_inputDirectory + file )
                else:
                    for file in self.files_outputFile:
                        outputFiles.append( self.files_outputDirectory + self.files_outputFile[0]+"."+self.files_outputExtension )
            i = 0
            for option in self.options.keys():
                if self.options[option].state:
                    #appends option name
                    if option != "pipeTo" and option != "logToFile":
                        arguments.append( str(self.options[option].optionPrefix + option) )
                        if self.options[option].paramTypeString == "float3":
                            arguments.append( str( self.options[option].param.value[0][0] ) )
                            arguments.append( str( self.options[option].param.value[0][1] ) )
                            arguments.append( str( self.options[option].param.value[0][2] ) )
                        elif self.options[option].paramTypeString == "Boolean":
                            if not self.options[option].param.boolAsString:
                                if self.options[option].param.value[0] == "True":
                                    arguments.append( "1" )
                                else:
                                    arguments.append( "0" )
                            else:
                                arguments.append( str( self.options[option].param.value[0] ) )
                        elif self.options[option].param.value[0]=="":
                            pass
                        else:
                            arguments.append( str( self.options[option].param.value[0] ) )
                    else:
                        postArguments.append(str(self.options[option].optionPrefix))
                        postArguments.append(str( self.options[option].param.value[0]))

            import copy
            tmpCmd = []
            self.fullCmdCommand = []
            """
            #===================================================================
            if input and not multipleInput and not output
                cmd --options input1
                cmd --options input2
                cmd --options input3

            elif input and multiple input and no output
                cmd --options input1 input2 input3

            elif not input and output
                cmd --options output1

            elif input and multiple input and output
                cmd --options input1 input2 input3 output1

            elif input and output
                cmd --options input1 output1
                cmd --options input2 output2

            else
                warning, check your xml conf input and output options!!!
            #===================================================================
            """
            if   self.inputFile and not self.multipleinputFiles and not self.outputFile:
                print "cmd --options input1"
                print "cmd --options input2"
                for i in range( 0,len( inputFiles ) ):
                    tmpCmd = copy.copy( arguments )
                    tmpCmd.insert( 0,argumentCmd )
                    tmpCmd.append( inputFiles[i] )
                    for post in range( 0,len( postArguments ) ):
                        tmpCmd.append(postArguments[post])
                    self.fullCmdCommand.append( tmpCmd )

            elif self.inputFile and self.multipleinputFiles and not self.outputFile:
                print "cmd --options input1 input2 input3"
                tmpCmd = copy.copy( arguments )
                tmpCmd.insert( 0,argumentCmd )
                for i in range( 0,len( inputFiles ) ):
                    tmpCmd.append( inputFiles[i] )
                for post in range( 0,len( postArguments ) ):
                        tmpCmd.append(postArguments[post])
                self.fullCmdCommand.append( tmpCmd )

            elif not self.inputFile and self.outputFile:
                print "cmd --options output"
                tmpCmd = copy.copy( arguments )
                tmpCmd.insert( 0,argumentCmd )
                tmpCmd.append( outputFiles[0] )
                for post in range( 0,len( postArguments ) ):
                        tmpCmd.append(postArguments[post])
                self.fullCmdCommand.append( tmpCmd )

            elif self.inputFile and self.multipleinputFiles and self.outputFile:
                print "cmd --options input1 input2 input3 output1"
                tmpCmd = copy.copy( arguments )
                tmpCmd.insert( 0,argumentCmd )
                for i in range( 0,len( inputFiles ) ):
                    tmpCmd.append( inputFiles[i] )
                tmpCmd.append( outputFiles[0] )
                for post in range( 0,len( postArguments ) ):
                        tmpCmd.append(postArguments[post])
                self.fullCmdCommand.append( tmpCmd )

            elif self.inputFile and not self.multipleinputFiles and self.outputFile:
                print "cmd --options input1 output1"
                print "cmd --options input2 output2"
                for i in range( 0,len( inputFiles ) ):
                    tmpCmd = copy.copy( arguments )
                    tmpCmd.insert( 0,argumentCmd )
                    tmpCmd.append( inputFiles[i] )
                    tmpCmd.append( outputFiles[i] )
                    for post in range( 0,len( postArguments ) ):
                        tmpCmd.append(postArguments[post])
                    self.fullCmdCommand.append( tmpCmd )
            for line in self.fullCmdCommand:
                print line

#            if self.inputFile:
#                if self.multipleOutputFiles:
#                    for i in range( 0,len( inputFiles ) ):
#                        print "ACAAAA!1"
#                        tmpCmd = copy.copy( arguments )
#                        tmpCmd.insert( 0,argumentCmd )
#                        tmpCmd.append( inputFiles[i] )
#                        tmpCmd.append( outputFiles[i] )
#                        self.fullCmdCommand.append( tmpCmd )
#                        SleepProgress( self.fullCmdCommand )
#                elif not self.multipleOutputFiles:
#                    print "ACAAAA!11"
#                    tmpCmd = copy.copy( arguments )
#                    tmpCmd.insert( 0,argumentCmd )
#                    for i in range( 0,len( inputFiles ) ):
#                        tmpCmd.append( inputFiles[i] )
#                    self.fullCmdCommand.append( tmpCmd )
#                    SleepProgress( self.fullCmdCommand )
#                else:
#                    print "ACAAAA!2"
#                    tmpCmd = copy.copy( arguments )
#                    tmpCmd.insert( 0,argumentCmd )
#                    for i in range( 0,len( inputFiles ) ):
#                        tmpCmd.append( inputFiles[i] )
#                    tmpCmd.append( outputFiles )
#                    self.fullCmdCommand.append( tmpCmd )
#                    SleepProgress( self.fullCmdCommand )
#            else:
#                print "ACAAAA!3"
#                tmpCmd = copy.copy( arguments )
#                tmpCmd.insert( 0,argumentCmd )
#                tmpCmd.append( outputFiles[0] )
#                self.fullCmdCommand.append( tmpCmd )
#                SleepProgress( self.fullCmdCommand )








class commandOption( object ):
    def __init__( self,paramTypeString,state,index,list,prefix ):
        """
        --------------------------------------------------------------------------
        --------------------------creates option objects--------------------------
        --------------------------------------------------------------------------
        takes the arguments paramString type:
                                            fixedString
                                            string
                                            Integer
                                            float
                                            float3
                                            Boolean
        """
        self.state = state
        self.optionPrefix = prefix
        if state == "True":
            self.state = True
        elif state == "False":
            self.state = False
        self.paramTypeString = paramTypeString
        if paramTypeString == "fixedString":
            self.param = commandOptionType_fixedString( index,list )
            self.paramType = type( "" )
        elif paramTypeString == "string":
            self.param = commandOptionType_string( index,list )
            self.paramType = type( "" )
        elif paramTypeString == "Integer":
            self.param = commandOptionType_integer( index,list )
            self.paramType = type( 1 )
        elif paramTypeString == "float":
            self.param = commandOptionType_float( index,list )
            self.paramType = type( 1.0 )
        elif paramTypeString == "Boolean":
            self.param = commandOptionType_bool( index,list )
            self.paramType = type( True )
        elif paramTypeString == "float3":
            self.param = commandOptionType_float3( index,list )
            self.paramType = type( 1.0 )
        else:
            print "no param created!"

class commandOptionType_fixedString ( object ):
    """
    --------------------------------------------------------------------------
    ------------------------creates optionType object-------------------------
    --------------------------------------------------------------------------
    """
    def __init__( self,index,list ):
        self.list = list
        self.index = index
        self.value = [list[index]]
    def set_index( self,index = 0 ):
        try:
            self.index = index
            self.value = [self.list[index]]
        except:
            print "set_index: outta range!!. Got: ",index
    def set_value ( self,value ):
        print "set_value: nothing to set here(None). Got: ",value
    def set_valueFromString ( self,valueString ):
        try:self.set_index( self.list.index( valueString ) )
        except:print "commandOptionType_fixedString.set_valueFromString(): notFount!in list"


class commandOptionType_string ( object ):
    """
    --------------------------------------------------------------------------
    ------------------------creates optionType object-------------------------
    ---------------------------------string-----------------------------------
    --------------------------------------------------------------------------
    """
    def __init__( self,index,list ):
        self.list = list
        self.index = 0
        self.value = [list[index]]
    def set_index( self,index = 0 ):
        pass
    def set_value ( self,value ):
        if type( value ) == str:
            self.value = [value]
            self.list = [value]
        else:print "set_value: type error while set_value(str), not str. Got: ",value
    def set_valueFromString ( self,valueString ):
        try:
            if type( valueString ) == str:
                self.set_value( valueString )
        except:
            print "commandOptionType_fixedString.set_valueFromString(): notString?"


class commandOptionType_integer ( object ):
    """
    --------------------------------------------------------------------------
    ------------------------creates optionType object-------------------------
    ---------------------------------integer----------------------------------
    --------------------------------------------------------------------------
    """
    def __init__( self,index,list ):
        self.list = list
        self.index = 0
        self.value = [list[index]]
    def set_index( self,index = 0 ):
        pass
    def set_value ( self,value ):
        if type( value ) == int:self.value = [value]
        else:print "set_value: type error while set_value(int), not int. Got: ",value

class commandOptionType_float ( object ):
    """
    --------------------------------------------------------------------------
    ------------------------creates optionType object-------------------------
    ---------------------------------float------------------------------------
    --------------------------------------------------------------------------
    """
    def __init__( self,index,list ):
        self.list = list
        self.index = 0
        self.value = [list[index]]
    def set_index( self,index = 0 ):
        pass
    def set_value ( self,value ):
        if type( value ) == float: self.value = [value]
        else:print "set_value: type error while set_value(float), not float. Got: ",value

class commandOptionType_float3 ( object ):
    """
    --------------------------------------------------------------------------
    ------------------------creates optionType object-------------------------
    --------------------------------float3------------------------------------
    --------------------------------------------------------------------------
    """
    def __init__( self,index,list ):
        self.list = list
        self.index = 0
        self.value = [list]
    def set_index( self,index = 0 ):
        pass
    def set_value ( self,value ):
        try:
            print value
            if type( value[0] ) == float:self.value = [value]
        except:
            print "set_value: type error while set_value(float3), not [float, float, float]. Got: ",value

class commandOptionType_bool ( object ):
    """
    --------------------------------------------------------------------------
    ------------------------creates optionType object-------------------------
    ---------------------------------bool-------------------------------------
    --------------------------------------------------------------------------
    """
    def __init__( self,index,list ):
        self.list = list
        self.index = index
        self.value = [list[index]]
        self.boolAsString = False
    def set_index( self,index = 0 ):
        try:
            self.index = index
            self.value = [self.list[index]]
        except:
            print "set_index: outta range!!. Got: ",index
    def set_value ( self,value ):
        print "set_value: nothing to set here(None)"
    def set_valueFromString ( self,valueString ):
        value = False
        if valueString == "True":value = True
        self.set_index( self.list.index( valueString ) )


