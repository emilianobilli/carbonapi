## @brief CarbonJob() Class
#
# Author: Emiliano Billi
#
#
# TODO: - Extrac error and warnings in __LoadXml()
#	- Documentation
#
#
#
#
from libhemam.Carbon.CarbonSocketLayer import *
from libhemam.Carbon.CarbonUtils import *
from xml.etree.ElementTree import *


class JobStatusListCriteria(object):
    def __init__(self, parameter = None, operator = None, value = None):
	self.Parameter = parameter
	self.Operator  = operator
	self.Value     = value

# Example 
# criteria_1 = JobStatusListCriteria("Status", "EQUAL", "COMPLETED)
#

class JobStatusListSettings(object):
    def __init__(self, orderby = None, orderbydirection = None, limitstart = None, limitshow = None):
	self.OrderBy = orderby
	self.OrderByDirection = orderybydirection
	self.LimitStart_DWD = limitstart
	self.LimitShow_DWD = limitshow


# Return a list of Jobs
def JobStatusList(carbon, JobStatusListCriteria=[], JobStatusListSettings=None):
 
    Jobs = []

    xmlheader = "<?xml version=\"1.0\"?>"

    cnpsXML = Element("cnpsXML")
    cnpsXML.attrib["CarbonAPIVer"] ="1.2"
    cnpsXML.attrib["TaskType"] = "JobStatusList"

    Filter = Element("Filter")

    i = 0
    for criteria in JobStatusListCriteria:
        criteria_n = Element("Criteria_" + str(i))
        criteria_n.attrib["Parameter"] = criteria.Parameter
        criteria_n.attrib["Operator"]   =  criteria.Operator
        criteria_n.attrib["Value"]        = criteria.Value
        i = i + 1
        Filter.append(criteria_n)

    cnpsXML.append(Filter)

    ListSettings = Element("ListSettings")
    if JobStatusListSettings is not None:	
        ListSettings.attrib["OrderBy"] = JobStatusListSettings.OrderBy
        ListSettings.attrib["OrderByDirection"] = JobStatusListSettings.OrderByDirection
        ListSettings.attrib["LimitStart.DWD"] = JobStatusListSettings.LimitStart_DWD
        ListSettings.attrib["LimitShow.DWD"] = JobStatusListSettings.LimitShow_DWD

    cnpsXML.append(ListSettings)
           
    xml = xmlheader + tostring(cnpsXML, encoding="utf-8")

    replyXml = carbon.SendXml(xml)	


    replyElement = fromstring(replyXml)
	
    if replyElement.tag == "Reply":

        if replyElement.get("Success") == "TRUE":
	    
	    JobStatusListTag = replyElement.find("JobStatusList")
	    
	    if JobStatusListTag is not None:
		NrOfJobsStr = JobStatusListTag.get("NrOfJobs.DWD")
		if NrOfJobsStr is not None:
		    NrOfJobs = int(NrOfJobsStr)
		
                    i = 0
		    Jobs = []
		    while ( i <= NrOfJobs-1 ):
			job_n = JobStatusListTag.find("Job_" + str(i))
			
			Jobs.append(CarbonJob(carbon, JobXmlElement=job_n))	
  	
			i = i + 1
	
		
    return Jobs		


def StartJobStandAlone(carbon = None, XmlCarbonApi = None):
	if carbon is not None:
		if XmlCarbonApi is not None:
			reply = carbon.SendXml(XmlCarbonApi)
			print reply
			replyElement = fromstring(reply)
			if replyElement.tag == "Reply":
				if replyElement.get("Success") == "TRUE":
					return CarbonJob(carbon, replyElement.get("GUID"))
				else:
					return None
			
    


class CarbonJob(object):

        def __init__(self, carbon = None, GUID=None, JobXmlElement=None):
                self.__CarbonSocket = carbon

                self.__plainReply   = ""
                self.__Running      = False

		self.__Name	    = ""
                self.__GUID         = ""
                self.__State        = ""
                self.__Status       = ""
                self.__Progress     = 0
                self.__Description  = ""
                self.__User         = ""
                self.__SourceDescription = ""
                self.__JobGuid      = ""
                self.__Priority_DWD = 0
                self.__DeleteProcessedSource_DWD = 0
                self.__CheckTime    = ""
                self.__StartTime    = ""

                self.__errors       = []
                self.__warnings     = []

                
		if GUID is not None:
			self.__GUID    = GUID
			self.__Running = True
			self.__Update()		
	
		elif JobXmlElement is not None:
			self.__Running = True
			self.__loadfromElement(JobXmlElement)



	## SetCarbon():
	# @brief Set a CarbonSocketLayer 
	# @param self The self object pointer
	# @param carbon A CarbonSocketLayer Object
	def SetCarbon(self, carbon = None):
		self.__CarbonSocket = carbon

	## Start():
	# @brief Send the xml to a carbon and update attributes
	# @param self The self object pointer
	# @retval boolen True or False
#	def Start(self):
#		if self.__xmlCommand != "" and self.__CarbonSocket != None:
#			reply = self.__CarbonSocket.SendXml(self.__xmlCommand)
#			ok, other = self.__EvaluateSuccess(reply)
#			if ok == True:
#				self.__GUID    = other
#				print other
#				self.__Running = True 
#				self.__Update()
#				return True
#			else:
#				self.__errors.append(other)
#				return False		
#
#		else:
#			return False


	def WaitFinnish(self, wait_loop = 10):
		pass


	def __EvaluateSuccess(self, xml=""):
		if xml != "":
			reply = fromstring(xml)
			if reply.tag == "Reply":
				if reply.get("Success") == "TRUE":
					return True, reply.get("GUID")
				else:
					return False, reply.get("Error")
		
		return False, "(EvaluateSuccess): XML is empty"


	def __LoadData(self, JobInfo = None):

		if JobInfo != None:
                        self.__Name         = JobInfo.get("Name")
                        self.__State        = JobInfo.get("State")

                        self.__Status       = JobInfo.get("Status")
                        progress            = JobInfo.get("Progress.DWD")
                        if progress != None:
                                self.__Progress     = int(progress)

                        self.__Description  = JobInfo.get("Description")
                        self.__User         = JobInfo.get("User")
                        self.__SourceDescription = JobInfo.get("SourceDescription")
                        self.__JobGuid      = JobInfo.get("Guid")
                        self.__GUID         = self.__JobGuid
                        self.__Priority_DWD = int(JobInfo.get("Priority.DWD"))

                        deleteprocessedsource = JobInfo.get("DeleteProcessedSource.DWD")
                        if deleteprocessedsource is not None:
                                self.__DeleteProcessedSource_DWD = int(deleteprocessedsource)
                        self.__CheckTime    = JobInfo.get("CheckTime")
                        self.__StartTime    = JobInfo.get("StartTime")

                        Failures = JobInfo.find("Failures")
                        if Failures is not None:

                                Errors   = Failures.find("Errors")
                                if Errors is not None:
                                        error_n = Errors.find("Error_0")
                                        if error_n is not None:
                                                self.__errors.append(error_n.get("Error"))


	def __loadfromXmlReply(self, xml):
		reply = fromstring(xml)
		if reply.tag == "Reply":
			self.__plainReply = xml
			JobInfo = reply.find("JobInfo")
			self.__LoadData(JobInfo)

	def __loadfromElement(self, Job_n):
		self.__LoadData(Job_n)



	def __Update(self):
		if self.__Running == True:
			xml = CreateCarbonXMLJobCommand("QueryInfo", self.__GUID)
			reply = self.__CarbonSocket.SendXml(xml)
			ok, other = self.__EvaluateSuccess(reply)
			if ok == True:
				self.__loadfromXmlReply(reply)
			else:
				self.__errors.append(other)
		

	def __AllCommands(self, cmd=""):
		if cmd != "" and self.__Running == True:
			xml = CreateCarbonXMLJobCommand(cmd, self.__GUID)
			reply = self.__CarbonSocket.SendXml(xml)
			ok, other = self.__EvaluateSuccess(reply)
			if ok == True:
				return True
			else:
				self.__errors.append(other)
				return False


	def Stop(self):
		return self.__AllCommands("Stop")				

	def Pause(self):
		return self.__AllCommands("Pause")

    	
	def Resume(self):
		return self.__AllCommands("Resume")


	def SetPriority(self, priority="5"):
		if self.__Running == True:
			xml = CreateCarbonXMLJobCommand("SetPriority", self.__GUID, priority)
			reply = self.__CarbonSocket.SendXml(xml)
			ok, other = self.__EvaluateSuccess(reply)
			if ok == True:
				return True
			else:
				self.__errors.append(other)
				return False
	

	def Requeue(self):
		return self.__AllCommands("Requeue")


	def Remove(self):
		return self.__AllCommands("Remove")


	def GetName(self):
		return self.__Name

	
	def GetGUID(self):
		return self.__GUID


	def GetState(self, update = False):
		
		if self.__Running == False:
			return None

		if update == True:
			self.__Update()

		return self.__State
		

	def GetStatus(self, update = False):
		
		if self.__Running == False:
			return None

		if update == True:
			self.__Update()

		return self.__Status


	def GetProgress(self, update = False):
				
		if self.__Running == False:
			return None

		if update == True:
			self.__Update()

		return self.__Progress


	def GetDescription(self, update = False):
		
		if self.__Running == False:
			return None

		if update == True:
			self.__Update()

		return self.__Description


	def GetSourceDescription(self, update = False):
		
		if self.__Running == False:
			return None

		if update == True:
			self.__Update()

		return self.__SourceDescription

	
	def GetUser(self, update = False):
		
		if self.__Running == False:
			return None

		if update == True:
			self.__Update()

		return self.__User

	def GetJobGuid(self, update = False):
		
		if self.__Running == False:
			return None

		if update == True:
			self.__Update()

		return self.__JobGuid


	def GetPriority(self, update = False):
		
		if self.__Running == False:
			return None

		if update == True:
			self.__Update()

		return self.__Priority_DWD

	
	def GetDeleteProcessedSource(self, update = False):
		
		if self.__Running == False:
			return None

		if update == True:
			self.__Update()

		return self.__DeleteProcessedSource_DWD

	
	def GetCheckTime(self, update = False):
		
		if self.__Running == False:
			return None

		if update == True:
			self.__Update()

		return self.__CheckTime

	
	def GetStartTime(self, update = False):
		
		if self.__Running == False:
			return None

		if update == True:
			self.__Update()

		return self.__StartTime


	def GetErrors(self):
		return self.__errors


	def GetWarnings(self):
		return self.__warnings


	def GetPlainReply(self):
		return self.__plainReply



