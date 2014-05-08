cmdPyWrapper
============

An xml based command line wrapper.

tired of command lines? loong arguments? repetitive tasks on the console? At least i was...
This PyQt window will parse a xml with the arguments, argument types, values, and default values for any command specified and build up a dynamic interface according to what you selected. example xml includes configuration for: tdlmake, txmake, ptfilter, ptmerge, brickmake, imageMagik convert with all posible command arguments taken from the help see the whole post!: … This are some screenshots of the xml setup for 3delight tdlmake, shaderdl, and envTexture.

It is an old project, that would need some serious TLC. Works as is, so no near future plans to enhance it.


XML EXAMPLE for 3delight ptcmergessss:
---------------------------------

<cmdsroot>
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
</cmdsroot>
