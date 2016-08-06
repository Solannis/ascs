#!/usr/bin/python
#
#   Repository: Astromech Secure Control System
#    Component: Command Line Argument Parser
#      Version: 0.1
# Date Created: 02-Aug-2016 MBF
# Date Updated: 02-Aug-2016 MBF
#

import sys

#=========================#
# Define global variables #
#=========================#
GLOBAL_HOST = ""                # Host name
GLOBAL_TYPE = "master"          # By default, the software will run as "master"  
GLOBAL_PORT = 49152             # Host port nubmer (to listen on)
GLOBAL_CONN = 5                 # Connection count (how many simultaneous connections are allowed)
GLOBAL_RECV_BUFF = 4096         # Receive buffer size limit (how much data in a single packet)

#===================#
# Class Definitions #
#===================#

#----------------------------------------#
# Class: Command Line Argument Processor #
#----------------------------------------#
#
# Command Line Argument Processor ('Clap' for short) will look for, accept, and parse
# command line arguments.
#

class Clap:
    'Command Line Argument Processor (Clap for short)'
    
    #
    # Valid command line parameters:
    #
    # -type:<master|remote>
    #   As an alternative to the -master and -remote flags (and uncomplicating the 
    #   possible conflict of using them both on the same command line), it will be much
    #   easier to use a -type flag with a value of master or remote. This way, there
    #   is only the one detection, and if another one is used in the same command
    #   line, it's still part of one detection instead of having two detections and
    #   essentially all the same branching for both.
    #
    #   The differences between master and remote are as follows.
    #
    #       master
    #           This is the head unit. The attributes associated with being the 
    #           master server are:
    #               1) The master server runs an additional listener to receive 
    #                   instructions from the control interface client.
    #               2) The master server only reads the config_devices_master.xml file.
    #               3) The master server must be started before starting the remote 
    #                   server.
    #           By definition, if the software is running as master, it cannot be a 
    #           remote.
    #
    #       remote
    #           This is the slave unit. The attributes associated with being the
    #           remotes server are: 
    #               1) The remote server only connects to the master server. It
    #                   does not connect with the control interface client (user).
    #               2) The remote server only loads the config_devices_remote.xml file.
    #               3) The remote server is started up only after the master server is
    #                   already up and running.
    #
    # -port:<numeric value>
    #   This value will override the defailt GLOBAL_PORT value defined above. This must
    #   be a valid port number from 49152 through 65535.
    #
    
    #--------------------------#
    # Function: Initialization #
    #--------------------------#
    #
    # Object initialization function
    #
    def __init__(self):
        self.parameters = {}
    
    #---------------------------#
    # Function: Parse Arguments #
    #---------------------------#
    #
    # Break the arguments into their parameter/value pairs
    #
    def ParseArguments(self):
        #
        # Select each argument for processing
        #
        for argument in sys.argv:
            #
            # Check to see if it's the executed filename with a .py file extension.
            #
            if (argument.find(".py", 0) == -1):
                #
                # Check to see which parameter it is:
                #
                if (argument.find("-type", 0) > -1):
                    #
                    # The -type argument was found. Check to see if another -type
                    # parameter was already provided.
                    #
                    if (self.parameters.has_key('type')):
                        #
                        # Type has already been set. Display an error message to
                        # that effect.
                        #
                        print "Error PA1-1: Master/Remote type has already been set to:", self.parameters['type']
                        print "\tTo change this server type, restart the server with the desired type argument."
                    else:
                        #
                        # Type has not been set. First, find the parameter value and
                        # force it to all lower case.
                        #
                        typeString = argument[(argument.find(":", 0) + 1):len(argument)].lower()
                        #
                        # Now check to see if it is a valid value, matching either
                        # master or remote.
                        #
                        if ((typeString == 'master') or (typeString == 'remote')):
                            #
                            # Matched either master or remote, so continue on with
                            # this as a valid parameter value. Add the type key and
                            # type value to the parameter dictionary and display
                            # an acknowledgement message.
                            #
                            self.parameters['type'] = typeString
                            print "ParseArguments: Server type has been set to:", self.parameters['type']
                        else:
                            #
                            # Did not match a valid parameter type. Display an
                            # error message to that effect.
                            #
                            print "Error PA1-2: Invalid server type:", typeString
                            print "\tPlease specify either \'master\' or \'remote\'."
                elif (argument.find("-port",0) > -1):
                    #
                    # First, find the parameter value.
                    #
                    portString = argument[(argument.find(":",0)+1):len(argument)]
                    #
                    # Now check it to see if it is a valid numeric value (even in
                    # string form).
                    #
                    if (portString.isdigit()):
                        #
                        # The string represents a valid numeric value. Now grab the
                        # numeric value.
                        #
                        portValue = int(portString)
                        #
                        # Check the value to make sure it is within the valid range
                        # of port values (between 49152 and 65535 inclusive).
                        #
                        if ((portValue > 49151) and (portValue < 65536)):
                            #
                            # Value is within valid range. Add the port key and the
                            # port value to the parameter dictionary and display an
                            # acknowledgement message.
                            #
                            self.parameters['port'] = portValue
                            print "ParseArguments: Port value has been set to:", self.parameters['port']
                        else:
                            #
                            # The value was a valid number, but not within the 
                            # designated range of valid port numbers. Display
                            # an error message to that effect.
                            #
                            print "Error PA2-1: Invalid port value:", portValue
                            print "\tPlease use a numeric value between 49152 and 65535."
                    else:
                        #
                        # The value was not a valid number to begin wtih. Display
                        # an error message to that effect.
                        #
                        print "Error PA2-2: Port value is non-numeric:", portString
                        print "\tPlease use a numeric value between 49152 and 65535."
        
        #
        # All arguments have now been parsed. Backfill any missing parameters with
        # global default values.
        #
        if (self.parameters.has_key('host') == False):
            self.parameters['host'] = GLOBAL_HOST
        if (self.parameters.has_key('type') == False):
            self.parameters['type'] = GLOBAL_TYPE
        if (self.parameters.has_key('port') == False):
            self.parameters['port'] = GLOBAL_PORT
        if (self.parameters.has_key('conn') == False):
            self.parameters['conn'] = GLOBAL_CONN
        if (self.parameters.has_key('recv_buff') == False):
            self.parameters['recv_buff'] = GLOBAL_RECV_BUFF
        
        #print self.parameters
   
    #-------------------------#
    # Function: Get Arguments #
    #-------------------------#
    #
    # Return the parameters dictionary to the caller
    #
    def GetArguments(self):
        return self.parameters
    
#
# END OF CLASS
# Class: Command Line Argument Processor #
#----------------------------------------#
