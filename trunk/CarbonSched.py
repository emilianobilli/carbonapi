from carbonapi.CarbonSocketLayer import *
from carbonapi.CarbonJob import *

import sys
import os
import time

class JobCarbonPoolReply(object):
    def __init__(self):
	self.Result = False
	self.Job    = None
	self.Error  = False


def StartJobCarbonPool(CarbonSet = None, XmlCarbonApi = None, AlwaysSchedule = True):

    JobReply = JobCarbonPoolReply()

    if CarbonSet.poolLen() == 0:
	JobReply.Error  = True
	JobReply.Result = False		

    if CarbonSet is not None:

	if XmlCarbonApi is not None:
			
	    Carbon = CarbonSet.GetBestCarbon(AlwaysSchedule)
	    if Carbon is not None:
		JobReply.Job =  StartJobStandAlone(Carbon, XmlCarbonApi)
	        if JobReply.Job is not None:
		    JobReply.Result = True
		    JobReply.Error  = False
		else:
		    JobReply.Result = False
		    JobReply.Error  = True
	    else:
		if AlwaysSchedule == False:
		    JobReply.Result = False
		    JobReply.Error  = False
		    JobReply.Job    = None 
			    
	else:
	    JobReply.Error  = True
	    JobReply.Result = False
    else:
	JobReply.Error  = True
	JobReply.Result = False

    return JobReply

class CarbonStatus(object):
    def __init__(self, carbon=None):
	if carbon is not None:
	    self.carbon = carbon
	    self.JobsInProgress = 0
	    self.JobsInQueue    = 0
	    self.SchedValue	    = 0

	else:
	    return None

    def UpdateStatus(self, AlwaysSchedule=True):

    	self.JobsInProgress = 0
    	self.JobsInQueue    = 0
	self.SchedValue     = 0

	Jobs = JobStatusList(self.carbon)
	for job in Jobs:
	    status = job.GetStatus()
            if status == "QUEUED":
		self.JobsInQueue = self.JobsInQueue + 1
            elif status == "STARTED" or status == "STARTING":
                self.JobsInProgress = self.JobsInProgress + 1
	    else:
		pass

	if self.JobsInQueue > 0 and AlwaysSchedule:
	    self.SchedValue = (self.JobsInQueue / int(self.carbon.Slots_DWD)) * -1
	else:
	    self.SchedValue	= int(self.carbon.Slots_DWD) - self.JobsInProgress



class CarbonPool(object):
    def __init__(self):
	self.CarbonPoolList = []

    def poolLen(self):
	return len(self.CarbonPoolList)


    def addCarbon(self, hostname=None):
	exist = False
	if hostname is not None:
	    for carbon in self.CarbonPoolList:
		if carbon.carbon.hostname == hostname:
		    exist = True
	
	if exist == False:
	    carbon = CarbonSocketLayer(hostname)
	    if carbon.LoadNodeStatus():
		self.CarbonPoolList.append(CarbonStatus(carbon))
		return True
	    else:
		return False
	else:
	    return False


    def delCarbon(self, hostname=None):
        i = 0
        if hostname is not None:
	    for carbon in self.CarbonPoolList:
	        if carbon.carbon.hostname == hostname:
		    del(self.CarbonPoolList[i])
		    return True
		i = i + 1
	
	return False

    def GetBestCarbon(self, AlwaysSchedule = True):
	
        first = True
        Selected = None

        for Carbon in self.CarbonPoolList:
    	    Carbon.UpdateStatus(AlwaysSchedule)
    	    print "SCHED VALUE: " +  str(Carbon.SchedValue)
	    if first:
	        first = False
	        Selected = Carbon
	    else:
	        if Carbon.SchedValue > Selected.SchedValue:
	    	    Selected = Carbon
	
	if Selected is not None:
	    if Selected.SchedValue == 0 and AlwaysSchedule == False:
		return None
	    return Selected.carbon
		
	return None	


