#!/usr/bin/python
#
#   Repository: Astromech Secure Control System
#    Component: Secure Server
#      Version: 0.1
# Date Created: 01-Aug-2016 MBF
# Date Updated: 02-Aug-2016 MBF
#
# 02-Aug-2016
#   Completed CLAP functionality
#   Moved CLAP code into its own file, removed it from Secure Server, and added import statement to include it
#

import socket                   # Import the socket module
import threading                # Import the threading module
import sys
from clap import Clap

#=========================#
# Define global variables #
#=========================#
GLOBAL_HOST = ""                # Host name
GLOBAL_TYPE = "master"          # By default, the software will run as "master"  
GLOBAL_PORT = 49152             # Host port nubmer (to listen on)
GLOBAL_CONN = 5                 # Connection count (how many simultaneous connections are allowed)
GLOBAL_RECV_BUFF = 4096         # Receive buffer size limit (how much data in a single packet)
GLOBAL_WELCOME = "\nWelcome to Astromech Secure Control System v0.1\nPlease log in to get started."
                                # Welcome message string
GLOBAL_PASS = "Overweight Glob Of Grease"
                                # Master password
GLOBAL_PASS_SPECIAL = "bellybutton"
                                # Special password recognition #1

#===================#
# Class Definitions #
#===================#




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
print c.GetArguments()