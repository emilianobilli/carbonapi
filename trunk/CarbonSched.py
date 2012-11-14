from libhemam.Carbon.CarbonSocketLayer import *
from libhemam.Carbon.CarbonJob import *

import sys
import os
import time


def StartJobCarbonPool(carbonset = None, XmlCarbonApi = None):

	if carbonset is not None:
		if XmlCarbonApi is not None:
			carbon = carbonset.GetBestCarbon()
			return StartJobStandAlone(carbon, XmlCarbonApi)


class CarbonStatus(object):
	def __init__(self, carbon=None):
		if carbon is not None:
			self.carbon = carbon
			self.JobsInProgress = 0
			self.JobsInQueue    = 0
			self.SchedValue	    = 0

		else:
			return None

	def UpdateStatus(self):

		self.JobsInProgress = 0
		self.JbosInQueue    = 0
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

		if self.JobsInQueue > 0:
			self.SchedValue = (self.JobsInQueue / int(self.carbon.Slots_DWD)) * -1
		else:
			self.SchedValue	= int(self.carbon.Slots_DWD) - self.JobsInProgress


class CarbonPool(object):
	def __init__(self):
		self.CarbonPoolList = []

	def addCarbon(self, hostname=None):
		exist = False
		if hostname is not None:
			for carbon in self.CarbonPoolList:
				if carbon.carbon.hostname == hostname:
					exist = True
	
		if exist == False:
			self.CarbonPoolList.append(CarbonStatus(CarbonSocketLayer(hostname)))
			return True
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

	def GetBestCarbon(self):
	
		first = True
		selected = None

		for carbon in self.CarbonPoolList:
			carbon.UpdateStatus()
			if first:
				first = False
				selected = carbon
			else:
				if carbon.SchedValue > selected.SchedValue:
					selected = carbon
	
		if selected is not None:
			return selected.carbon
		
		return None	


