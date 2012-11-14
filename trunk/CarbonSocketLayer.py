## @brief
# Class CarbonSocketLayer: Interface to/from Rhozet Carbon Coder
#
# Author: Emiliano Billi 2010
#
# Changes: 
#	- Documentation: Emiliano Billi

from xml.etree.ElementTree import *
import socket


# @package CarbonSocketLayer(): Socket layer from Rhozet Carbon Coder 
class CarbonSocketLayer(object):
	def __init__(self, hostname=None, port=1120):
		self.socket = None
		self.error  = u""
		self.hdr    = "CarbonAPIXML1"
		self.hostname = hostname
		self.port     = port
		self.msg      = u""

		self.Version  = u""

		self.Enabled_DWD  = u""
                self.Priority_DWD = u""
                self.Slots_DWD    = u""


		self.GetVersion()
		self.GetNodeStatus()

	## SetHostname()
        #  @param self The object pointer.
	#  @param hostname Hostname
	def SetHostname(self, hostname):
		self.hostname = hostname



	def GetVersion(self):
		cnpsXML = Element("cnpsXML")
        	cnpsXML.attrib["CarbonAPIVer"] = "1.2"
        	cnpsXML.attrib["TaskType"]     = "Version"
		xml = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>' + tostring(cnpsXML, encoding="utf-8")
		replyXml = self.SendXml(xml)
		reply = fromstring(replyXml)
                if reply.tag == "Reply":
                	if reply.get("Success") == "TRUE":
                        	self.Version = reply.get("Version")
			else:
				return None
	

	def GetNodeStatus(self):
		cnpsXML = Element("cnpsXML")
                cnpsXML.attrib["CarbonAPIVer"] = "1.2"
                cnpsXML.attrib["TaskType"]     = "NodeCommand"
		NodeCommand = Element("NodeCommand")
		NodeCommand.attrib["Command"] = "GetNodeStatus"
		NodeCommand.attrib["NodeIP"]  = self.hostname
		cnpsXML.append(NodeCommand)
                xml = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>' + tostring(cnpsXML, encoding="utf-8")
                replyXml = self.SendXml(xml)
                reply = fromstring(replyXml)
                if reply.tag == "Reply":
		
	                if reply.get("Success") == "TRUE":
				NodeStatus = reply.find("NodeStatus")                
				if NodeStatus is not None:
			
					self.Enabled_DWD  = NodeStatus.get("Enabled.DWD")
					self.Priority_DWD = NodeStatus.get("Priority.DWD")
					self.Slots_DWD    = NodeStatus.get("Slots.DWD")
	


	def SetNodeStatus(self, Enabled_DWD = None, Priority_DWD = None, Slots_DWD = None):
		cnpsXML = Element("cnpsXML")
                cnpsXML.attrib["CarbonAPIVer"] = "1.2"
                cnpsXML.attrib["TaskType"]     = "NodeCommand"
                NodeCommand = Element("NodeCommand")
                NodeCommand.attrib["Command"] = "SetNodeStatus"
                NodeCommand.attrib["NodeIP"]  = self.hostname

		NodeStatus = Element("NodeStatus")
		if Enabled_DWD is not None:
			NodeStatus.attrib["Enabled.DWD"] = Enabled_DWD

		if Priority_DWD is not None:
			NodeStatus.attrib["Priority.DWD"] = Priority_DWD

		if Slots_DWD is not None:
			if type(Slots_DWD).__name__ == 'int':
				NodeStatus.attrib["Slots.DWD"] = str(Slots_DWD)
			else:
				NodeStatus.attrib["Slots.DWD"] = Slots_DWD

		NodeCommand.append(NodeStatus)
		cnpsXML.append(NodeCommand)
		xml = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>' + tostring(cnpsXML, encoding="utf-8")
                replyXml = self.SendXml(xml)
                reply = fromstring(replyXml)
                if reply.tag == "Reply":
                        if reply.get("Success") == "TRUE":
				self.GetNodeStatus()
				return True
			else:
				return False


	## SetPort()
        #  @param self The object pointer.
	#  @param port Port
	def SetPort(self, port):
		self.port     = port

	## GetHostname()
        #  @param self The object pointer.
	#  @retval Hostname
	def GetHostname(self):
		self.hostname

	## GetPort()
        #  @param self The object pointer.
        #  @retval Port
	def GetPort(self):
		self.port

	def __atomic_read(self, size = None):
    
	    if self.socket == None or size == None or size < 0:
		return None
    
	    buffer = ''
    
	    while len(buffer) < size:
		try:
		    chunk = self.socket.recv(size-len(buffer))
		    buffer = buffer + chunk
		except:
		    return None

	    return buffer

	def __atomic_write(self, buffer = None):
    
	    if self.socket == None or buffer == None:
		return 0
	
	    send_bytes = 0

	    while send_bytes < len(buffer):
		try:
		    n = self.socket.send(buffer[send_bytes:])
		    send_bytes = send_bytes + n
		except:
		    return 0

	    return send_bytes



	def __Connect(self):
		if self.socket == None:
			if self.hostname != None and self.port != None:
				try:
					self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					self.socket.connect( (self.hostname, self.port) )

				except socket.error, msg:
					self.socket = None
					self.error  = "Imposible conectarse [%s:%s]" % ( self.hostname, self.port ) 

			else:
				self.error = "Error: Hostname %s, Port %s" % (self.hostname, self.port) 


	def __Disconnect(self):
		self.socket.close()
		self.socket = None

	def __Read_until_space(self):
		buffer = ""
		char = ""
				

		if self.socket != None:
			while True:
				buffer = buffer + char
				char = self.__atomic_read(1)
				if char == " ":
					break

			return buffer

	## SendXml()
        #  @param self The object pointer.
        #  @param xml The XML Job
        #  @retval xml with the reply of carbon
	def SendXml(self, xml=None):
		
		self.msg = xml		
		reply = None

		if self.msg != None:
			buffer = self.hdr + " " + str(len(self.msg)) + " " + self.msg
			
			self.__Connect()

			if self.socket != None:

				n = self.__atomic_write(buffer)
				if n > 0:
				    header = self.__atomic_read(len(self.hdr)+1)
				    msglen = self.__Read_until_space()
				    if header != None and msglen != None:
					reply = self.__atomic_read(int(msglen))
				    else:
					self.error  = "Error de I/O en el socket"
				else:				
				    self.error  = "Error de I/O en el socket"


				self.__Disconnect()
	
										
		return reply		
