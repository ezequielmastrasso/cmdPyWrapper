import xml.dom.minidom
from odict import *

class init_xmlCmd_rev1( object ):

    def __init__( self,xmlFilePath,verbose = False ):
        """/----------------CMD-XMLSchema-rev-1---------------/
            cmdsRoot Attrs:[init_xmlCmd_rev='1']>
            |-- cmd1
            |   |-- cmdConfig
            |   |     |-- configParam
            |   |     |    `-- paramValue
            |   |     `-- cmdPath
            |   |          `-- c:\\programFiles\\3delight\\bin
            |   `-- cmdOptions
            |         |-- optionName
            |         |    |--type
            |         |    `--param
            |         |        |-- paramValue1
            |         |        |-- paramValue2
            |         `-- filter
            |              |--fixedString
            |              `--param
            |                  |-- box
            |                  |-- triangle
            |                  |-- gaussian
            |                  |-- catmull-rom
            |                  |-- bessel
            |                  `-- mitchell
            `-- cmd2
            |   |-- cmdConfig
            |   |     |-- configParam
            |   |     |    |-- ...
            |   |     |    `-- ...
            |   |     `-- configParam
            |   |          |-- ...
            |   |          |-- ...
            |   |          `-- ...
            |   `-- cmdOptions
            |        `-- optionName
            |              |--...
            |              `--...
            |                  |-- ...
            |                  |-- ...
            |                  `-- ...
            `-- cmd3
                |-- cmdConfig
                |     |-- configParam
                |     |    |-- ...
                |     |    `-- ...
                |     `-- configParam
                |          |-- ...
                |          |-- ...
                |          `-- ...
                `-- cmdOptions
                     `-- optionName
                           |--...
                           `--...
                               |-- ...
                               |-- ...
                               `-- ...
        
        /-----------------------Types----------------------/
        cmdConfigParamValues
        |-- False
        |-- True
        `-- String
        cmdOptionNameType
        |-- Boolean
        |-- Int
        |-- Float
        `-- fixedString
        
        cmdOptionsNameParamType:
        needsToMatch the parent optionNameType specified
        /--------------------XMLSchema---------------------/
        /---------------------END Of-----------------------/"""
        self.xmlFile = open( xmlFilePath,'r' )
        self.xmldom = xml.dom.minidom.parse( self.xmlFile )
        self.xml_cmds = self.xmlProcess_rev1( self.xmldom,verbose )
        self.cmds = []
        self.verbose = verbose
        for xml_cmd in self.xml_cmds:
            for xml_cmdName in xml_cmd.keys():
                self.cmdConfig,self.cmdOptions = self.init_xmlCmd_rev1( xml_cmd[xml_cmdName] )
                self.cmds.append( {str( xml_cmdName ): {"cmdConfig":self.cmdConfig,"cmdOptions":self.cmdOptions } } )
    def removeWhilespaceNodes( self,node,unlink = False ):
        """remove empty nodes from xml structure"""
        remove_list = []
        for child in node.childNodes:
            if child.nodeType == xml.dom.Node.TEXT_NODE and \
               not child.data.strip():
                remove_list.append( child )
            elif child.hasChildNodes():
                self.removeWhilespaceNodes( child,unlink )
        for node in remove_list:
            node.parentNode.removeChild( node )
            if unlink:
                node.unlink()
    def init_xmlCmd_rev1( self,xml_cmds_structure ):
        cmdConfigSource = xml_cmds_structure["cmdConfig"]
        cmdConfig = OrderedDict()
        for config in cmdConfigSource.keys():
            if cmdConfigSource[config] == "True":
                cmdConfig[config] = True
            elif cmdConfigSource[config] == "False":
                cmdConfig[config] = False
            else:
                cmdConfig[config] = cmdConfigSource[config]
        cmdOptionsSource = xml_cmds_structure["cmdOptions"]
        cmdOptions = OrderedDict()
        paramType = None
        for config in cmdOptionsSource.keys():
            config = str( config )
            if cmdOptionsSource[config].has_key( "param" ):
                param = cmdOptionsSource[config]["param"]
            else:
                param = None
            if cmdOptionsSource[config].has_key( "prefix" ):
                prefix = cmdOptionsSource[config]["prefix"]
            else:
                prefix="-"
            if cmdOptionsSource[config]["type"] == "fixedString":
                paramType = "fixedString"
            if cmdOptionsSource[config]["type"] == "string":
                paramType = "string"
            if cmdOptionsSource[config]["type"] == "Boolean":
                paramType = "Boolean"
                for i in range( 0,1 ):
                    if param[i] == "False":
                        param[i] = "False"
                    else:param[i] = "True"
            if cmdOptionsSource[config]["type"] == "Integer":
                paramType = "Integer"
                param[0] = int( param[0] )
            if cmdOptionsSource[config]["type"] == "Float":
                paramType = "float"
                param[0] = float( param[0] )
            if cmdOptionsSource[config]["type"] == "Float3":
                paramType = "float3"

            cmdOptions[config] = [
                                cmdOptionsSource[config]["state"],
                                #1.0,
                                paramType,
                                0,
                                param,
                                prefix
                            ]
        return cmdConfig,cmdOptions
    def xmlProcess_rev1( self,xml,verbose = False ):
        #Process the xml file for the xmlRev1
        #Returns a dict with the next schema
        #{cmdName1:{
        #           "cmdConfig"   : { 
        #                             "configName1","stringBooleanValue"
        #                             "configName1","stringBooleanValue"
        #                           }
        #           "cmdOptions"  : {
        #                             "optionName", { "type"  : "type":
        #                                             "param" : [param1, param2, param3]
        #                                           }
        #                           }      
        #          }
        #searchForCommandsRootElement
        if verbose:
            print "\n\n/---------------------------/"
            print "/__XML_struct_class__rev1___/"
            print "/_______LOADING_XML_________/"
            print "/---------------------------/"
        commandsRoot = xml.getElementsByTagName( "cmdsRoot" )[0]
        self.removeWhilespaceNodes( commandsRoot )
        cmds = []
        cmdN = -1
        for xml_cmd in commandsRoot.childNodes:
            cmdN = cmdN + 1
            cmds.append( {
                    xml_cmd.tagName:{
                                    "cmdConfig":OrderedDict(),
                                    "cmdOptions":OrderedDict()
                                    }
                                    } )
            if verbose:print "\n\nCOMMAND LOADED"
            #xml_cmd.tagName=tdlMakeConvert
            if verbose:print xml_cmd.tagName
            for xml_cmd_child in xml_cmd.childNodes:
                #process cmdConfig tag
                if xml_cmd_child.tagName == "cmdConfig":
                    if verbose: print "\n\tProcessing ConfigTag"
                    #process cmdConfig childs
                    for xml_cmd_config in xml_cmd_child.childNodes:
                        if verbose:print "\t\t----" + xml_cmd_config.tagName
                        if verbose:print "\t\t\t\t" + xml_cmd_config.firstChild.nodeValue
                        #add dict cmdConfig entrys and values 
                        cmds[cmdN][xml_cmd.tagName]['cmdConfig'][str( xml_cmd_config.tagName )] = str( xml_cmd_config.firstChild.nodeValue )

                if xml_cmd_child.tagName == "cmdOptions":
                    if verbose:print "\n\tProcessing optionsTag"
                    #process cmdOptions childs
                    for xml_cmd_options in xml_cmd_child.childNodes:
                        #option name - xml_cmd_options.tagName
                        if verbose:print "\t\t----" + xml_cmd_options.tagName
                        #add empty dict cmdOptions entrys
                        cmds[cmdN][xml_cmd.tagName]['cmdOptions'][xml_cmd_options.tagName] = OrderedDict()
                        for xml_cmd_option in xml_cmd_options.childNodes:
                            #option name - xml_cmd_options.tagName
                            if xml_cmd_option.tagName == "type":
                                if verbose:print "\t\t\t\t" + xml_cmd_option.tagName + "\t" + str( xml_cmd_option.firstChild.nodeValue )
                                cmds[cmdN][xml_cmd.tagName]['cmdOptions'][xml_cmd_options.tagName][xml_cmd_option.tagName] = xml_cmd_option.firstChild.nodeValue
                            elif xml_cmd_option.tagName != "param" and xml_cmd_option.tagName != "prefix":
                                if verbose:print "\t\t\t\t" + xml_cmd_option.tagName + "\t" + str( xml_cmd_option.firstChild.nodeValue )
                                cmds[cmdN][xml_cmd.tagName]['cmdOptions'][xml_cmd_options.tagName][xml_cmd_option.tagName] = xml_cmd_option.firstChild.nodeValue
                            elif xml_cmd_option.tagName == "prefix":
                                if verbose:print "\t\t\t\t" + xml_cmd_option.tagName + "\t" + str( xml_cmd_option.firstChild.nodeValue )
                                cmds[cmdN][xml_cmd.tagName]['cmdOptions'][xml_cmd_options.tagName][xml_cmd_option.tagName] = xml_cmd_option.firstChild.nodeValue
                            else:
                                cmds[cmdN][xml_cmd.tagName]['cmdOptions'][xml_cmd_options.tagName][xml_cmd_option.tagName] = []
                                for param in xml_cmd_option.childNodes:
                                    try:
                                        if verbose:print "\t\t\t\t\t" + param.firstChild.nodeValue
                                        cmds[cmdN][xml_cmd.tagName]['cmdOptions'][xml_cmd_options.tagName][xml_cmd_option.tagName].append( str( param.firstChild.nodeValue ) )
                                    except:
                                        if verbose:print "\t\t\t\t\t" + " \" \""
                                        cmds[cmdN][xml_cmd.tagName]['cmdOptions'][xml_cmd_options.tagName][xml_cmd_option.tagName].append( "" )

        if verbose:
            print "/---------------------------/"
            print "/__XML_struct_class__rev1___/"
            print "/---------END-OF------------/\n\n"
        return cmds
    
    def getCmds( self ):
        return self.cmds
