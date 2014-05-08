cmdPyWrapper
============

An xml based command line wrapper.

Tired of combersome long commands in the console, cmdPyWrapper was born. 

It takes an xml with the command, and all its arguments, their types and default values, and builds up a interface on the fly with checkboxs and input boxes to edit the final command. Check the screenshots to see it.


It is an old project, that would need some serious TLC. Works as is, so no near future plans to enhance it.


XML EXAMPLE for 3delight ptcmergessss:
---------------------------------

    <delight-ptcmerge>
            <cmdconfig>
                  <inputfile>True</inputfile>
                  <cmdpath>C:\Program Files\3Delight\bin</cmdpath>
                  <cmdfile>ptcmerge.exe</cmdfile>
                  <multipleinputfiles>True</multipleinputfiles>
                  <outputfile>True</outputfile>
                  <outputfileextension>ptc</outputfileextension>
            </cmdconfig>
            <cmdoptions>
                  <logtofile>
                        <prefix>></prefix>
                        <state>False</state>
                        <type>string</type>
                        <param>
                                <mode>/var/log/cmdPyWrapperStdout.log</mode>
                  </logtofile>
            </cmdoptions>
    </delight-ptcmerge>

