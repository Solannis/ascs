#!/usr/bin/python
#
#   Repository: Astromech Secure Control System
#    Component: Read Configuration module (server_readconfig.py)
#      Version: 0.1
# Date Created: 05-Aug-2016 MBF
# Date Updated: 05-Aug-2016 MBF
#
# 05-Aug-2016
#   I have replaced the built-in Python XML library with the third-party LXML library. Amongst many
#   reasons for doing so, the pretty_print output ability makes managing the writing of XML files
#   much easier. Using it for reading as well for consistency. The good news is that due to my
#   relatively simple implementation of XML commands, it was an easy replacement with almost zero
#   additional modification to my code. Getting the damn thing installed was an entirely different
#   adventure, however. Needed to install the pip command (which required the installaiton of the 
#   xcode command-line tools, then the installation of pip before I could install LXML).
#

from lxml import etree as ElementTree
#import xml.etree.cElementTree as ElementTree

class ReadConfig:
    def __init__(self):
        self.configFile = "ascs_config.xml"      # Default server config file name
        self.configTree = None                          # Internal XML Tree object
        self.configRoot = None                          # Internal XML Root object
        self.parameters = {}                            # Internal parameters object
    
    def ReadXML(self):
        self.configTree = ElementTree.parse(self.configFile)
        self.configRoot = self.configTree.getroot()
        #
        # Because I know what I am looking for (or at), I can make certain assumptions about
        # what the configuration XML file should and should not have. 
        #
        # I know that the root should have three children, and those three children should be:
        #   master, remote, client
        # and I know that each of those three children should have three children of their own:
        #   hostname, hostport, hostkeyfile
        #
        # Any missing child can be defaulted and written back out to the file.
        #
        for child in self.configRoot:
            for grandchild in child:
                keyName = child.tag + "_" + grandchild.tag
                print keyName
                self.parameters[keyName] = grandchild.text
        return self.parameters
        
class CheckConfiguration:
    def __init__(self):
        self.parameters = {}
        
    def CheckConfig(self, parameters):
        self.parameters = parameters
        if (self.parameters.has_key('master_hostname') == False):
            self.parameters['master_hostname'] = "Fred"
        if (self.parameters.has_key('master_hostport') == False):
            self.parameters['master_hostport'] = 50000
        if (self.parameters.has_key('master_hostkeyfile') == False):
            self.parameters['master_hostkeyfile'] = "ServerKey_private.PEM"
        if (self.parameters.has_key('rempte_hostname') == False):
            self.parameters['remote_hostname'] = "Barney"
        if (self.parameters.has_key('remote_hostport') == False):
            self.parameters['remote_hostport'] = 50001
        if (self.parameters.has_key('remote_hostkeyfile') == False):
            self.parameters['remote_hostkeyfile'] = "ServerKey_public.PEM"
        if (self.parameters.has_key('client_hostname') == False):
            self.parameters['client_hostname'] = "Wilma"
        if (self.parameters.has_key('client_hostport') == False):
            self.parameters['client_hostport'] = 50002
        if (self.parameters.has_key('client_hostkeyfile') == False):
            self.parameters['client_hostkeyfile'] = "ClientKey_public.PEM"
        if (self.parameters.has_key('type_servertype') == False):
            self.parameters['server_type'] = "master"
        return self.parameters
        
    def DisplayParameters(self, parameters):
        self.parameters = parameters
        print "Master:"
        print "\tmaster_hostname: %s" % (self.parameters['master_hostname'])
        print "\tmaster_hostport: %s" % (self.parameters['master_hostport'])
        print "\tmaster_hostkeyfile: %s" % (self.parameters['master_hostkeyfile'])
        print "Remote:"
        print "\tremote_hostname: %s" % (self.parameters['remote_hostname'])
        print "\tremote_hostport: %s" % (self.parameters['remote_hostport'])
        print "\tremote_hostkeyfile: %s" % (self.parameters['remote_hostkeyfile'])
        print "Client:"
        print "\tmaster_hostname: %s" % (self.parameters['client_hostname'])
        print "\tmaster_hostport: %s" % (self.parameters['client_hostport'])
        print "\tmaster_hostkeyfile: %s" % (self.parameters['client_hostkeyfile'])
        print "Type:"
        print "\tserver_type: %s" % (self.parameters['type_servertype'])

class WriteXML:
    def __init__(self):
        self.parameters = {}
        self.root = None
        self.tree = None
        
    def BuildXML(self, parameters):
        self.parameters = parameters
        self.root = ElementTree.Element('chatconfig')
        self.childMaster = ElementTree.SubElement(self.root, "master")
        self.childRemote = ElementTree.SubElement(self.root, "remote")
        self.childClient = ElementTree.SubElement(self.root, "client")
        self.childType = ElementTree.SubElement(self.root, "type")
        self.childMasterHostname = ElementTree.SubElement(self.childMaster, "hostname")
        self.childMasterHostname.text = self.parameters['master_hostname']
        self.childMasterHostport = ElementTree.SubElement(self.childMaster, "hostport")
        self.childMasterHostport.text = self.parameters['master_hostport']
        self.childMasterHostkeyfile = ElementTree.SubElement(self.childMaster, "hostkeyfile")
        self.childMasterHostkeyfile.text = self.parameters['master_hostkeyfile']
        self.childRemoteHostname = ElementTree.SubElement(self.childRemote, "hostname")
        self.childRemoteHostname.text = self.parameters['remote_hostname']
        self.childRemoteHostport = ElementTree.SubElement(self.childRemote, "hostport")
        self.childRemoteHostport.text = self.parameters['remote_hostport']
        self.childRemoteHostkeyfile = ElementTree.SubElement(self.childRemote, "hostkeyfile")
        self.childRemoteHostkeyfile.text = self.parameters['remote_hostkeyfile']
        self.childClientHostname = ElementTree.SubElement(self.childClient, "hostname")
        self.childClientHostname.text = self.parameters['client_hostname']
        self.childClientHostport = ElementTree.SubElement(self.childClient, "hostport")
        self.childClientHostport.text = self.parameters['client_hostport']
        self.childClientHostkeyfile = ElementTree.SubElement(self.childClient, "hostkeyfile")
        self.childClientHostkeyfile.text = self.parameters['client_hostkeyfile']
        
        self.tree = ElementTree.ElementTree(self.root)
        self.tree.write("output.xml", pretty_print=True)



if __name__ == "__main__":
    xr = XMLRead()
    configParameters = xr.ReadConfig()
    cc = CheckConfiguration()
    configParameters = cc.CheckConfig(configParameters)
    cc.DisplayParameters(configParameters)
    wx = WriteXML()
    wx.BuildXML(configParameters)

"""
print root[0].attrib
print root[1]

for child in root[0]:
    print child

"""