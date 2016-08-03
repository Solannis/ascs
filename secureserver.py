#!/usr/bin/python
#
#   Repository: Astromech Secure Control System
#  Application: Secure Server
#      Version: 0.1
# Date Created: 01-Aug-2016 MBF
# Date Updated: 01-Aug-2016 MBF
#

import socket                   # Import the socket module
import threading                # Import the threading module
import sys

#=========================#
# Define global variables #
#=========================#
GLOBAL_HOST = ""                # Host name
GLOBAL_PORT = 49152             # Host port nubmer (to listen on)
GLOBAL_CONN = 5                 # Connection count (how many simultaneous connections are allowed)
GLOBAL_RECV_BUFF = 4096         # Receive buffer size limit (how much data in a single packet)
GLOBAL_ISMASTER = True          # By default, the software will run as "master"  
GLOBAL_WELCOME = "\nWelcome to Astromech Secure Control System v0.1\nPlease log in to get started."
                                # Welcome message string
GLOBAL_PASS = "Overweight Glob Of Grease"
                                # Master password
GLOBAL_PASS_SPECIAL = "bellybutton"
                                # Special password recognition #1

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
    # -master
    #   Indiciates that this instance of the software is the head unit or master. There 
    #   are three differences bewtween the master server and the remote server. They are:
    #       1) The master server runs an additional listener to receive instructions 
    #           from the control interface client.
    #       2) The master server only reads the config_devices_master.xml file.
    #       3) The master server must be started before starting the remote server.
    #   By definition, if the software is running as master, it cannot be a remote.
    #
    # -remote
    #   Indicates that this instance of the software is the remote. As described above
    #   in the -master parameter, remotes only connect to the master and not to the
    #   control interface client (user). They also only load the config_devices_remote.xml
    #   file. Also, it is presumed that the remote is started up only after the master
    #   has been started.
    #
    # -type:<master|remote>
    #   As an alternative to the -master and -remote flags (and uncomplicating the 
    #   possible conflict of using them both on the same command line), it will be much
    #   easier to use a -type flag with a value of master or remote. This way, there
    #   is only the one detection, and if another one is used in the same command
    #   line, it's still part of one detection instead of having two detections and
    #   essentially all the same branching for both.
    #
    #   The differences between master and remote remain the same as above.
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
                if (argument == "-master"):
                    #
                    # The -master argument was found. Check to see if there is already a setting for
                    # the master key. If there is, that means that the server type
                    #
                    if (self.parameters.has_key('master')):
                        if (self.parameters['master'] == True):
                            serverType = "Master"
                        else:
                            serverType = "Remote"
                        print "ParseArguments: Master/Remote status has already been set to:", serverType
                        print "ParseArguments: To change this server type, restart the server with the desired type argument."
                    else:
                        self.parameters['master'] = True
                        self.parameters['remote'] = False
                elif (argument == "-remote"):
                    if (self.parameters.has_key('master')):
                        if (self.parameters['master'] == True):
                            serverType = "Master"
                        else:
                            serverType = "Remote"
                        print "ParseArguments: Master/Remote status has already been set to:", serverType
                        print "ParseArguments: To change this server type, restart the server with the desired type argument."
                    else:
                        self.parameters['master'] = False
                        self.parameters['remote'] = True
                elif (argument.find("-port",0) > -1):
                    portString = argument[(argument.find(":",0)+1):len(argument)]
                    portValue = int(portString)
                    self.parameters['port'] = portValue
        
        print self.parameters
                    

    
    

""""
    
#---------------------#
# Class: ServerSocket #
#---------------------#
#
# ServerSocket class represents the server/listener functionality.
#
class ServerSocket:
    'ServerSocket class represents the server/listener functionality'
    
    #
    # Initialization Method
    #
    def __init__(self, hostName, portNumber, connectionCount):
        self.serverSocket = socket.socket()         # Create socket object, assign it to variable
        self.hostName = socket.gethostname()        # Get hostname from the socket, assign it to variable
        self.hostPort = portNumber                  # Get port nubmer argument, assign it to variable
        self.connections = connectionCount          # Get connection count argument, assign it to variable
        print "Hostname: ", self.hostName

    #
    # Start the server
    #
    def ServerStart(self):
        self.serverSocket.bind((self.hostName, self.hostPort))  # Bind the socket to a port
        self.serverSocket.listen(self.connections)  # Turn on listening on that socket
        print '\n=========='
        print "Server: Started listening on host [%s] on port [%d]" % (self.hostName, self.hostPort)
    
    #
    # Listen for and accept new incoming connections
    #
    def ServerAccept(self):
        self.threadCount = 1
        while True:
            print 'Server: Waiting for new incoming connection'
            self.connectedSocket, self.connectedAddress = self.serverSocket.accept()
            print 'Server: Accepting new incoming conneciton'
            ch = ConnectionHandler(self.threadCount, self.connectedSocket, self.connectedAddress)
            ch.start()
            self.threadCount += 1
            
class ConnectionHandler (threading.Thread):
    'ConnectionHandler class to represent how connections are handled'
        
    def __init__(self, threadID, socket, address):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.connectedSocket = socket
        self.connectedAddress = address
        self.connectionID = "Connection Handler Thread [%d]:" % self.threadID
        print '----------'
        print "%s connected" % self.connectionID
        self.ChatStart()

    def ChatStart(self):
        self.connectedSocket.send(global_intro_message)
        while True:
            recv_data = self.connectedSocket.recv(global_recv_buffer)
            print "Received:", recv_data
            if (recv_data == "quit") or (recv_data == "exit"):
                break
#                self.connectedSocket.close()
#                sys.exit()
            elif (recv_data == global_special_password):
                self.connectedSocket.send("I am glad you are in on the joke, but that is not the correct password.")
            elif (recv_data == global_password):
                self.connectedSocket.send("Welcome to the system.")
            else:
                self.connectedSocket.send("Incorrect password. Please try again.")
        print "Shutting down."
        sys.exit()
        
    def SendMessage(self):
        print "%s sending message to client" % self.connectionID
        self.connectedSocket.send('Thank you for connecting.')
        self.connectedSocket.close
        print "%s connection closed" % self.connectionID

ss = ServerSocket(global_host, global_port, global_connections)
ss.ServerStart()
ss.ServerAccept()

"""

c = Clap()
c.ParseArguments()