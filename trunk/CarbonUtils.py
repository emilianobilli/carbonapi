##
# CarbonUtils: Utils funtions
#
# Author: Emiliano Billi 2010
#
# Changes:
#       - Documentation: Emiliano Billi
#	- 29/08/2010: Adding function CreateCarbonXMLJobCommand 

#@package CarbonUtils

from xml.etree.ElementTree import *
import time

__all__ = ["FramesToCarbonFramesUnit", "CreateCarbonXMLJob", "CreateCarbonXMLJobCommand", "MailNotify", "StichSource"]
    

def __init__(self):
    pass
    
## CreateCarbonXMLJobCommand(): Generate a XML Carbon JobCommand
#
# @param command One of ("Stop", "Pause", "Resume", "QueryInfo")
# @param guid Guid of de Job
# @param priority If command is "SetPriority" use this value
def CreateCarbonXMLJobCommand(command="", guid="", priority=255):

    if command != "" and guid != "":
	cnpsXML = Element("cnpsXML")
	cnpsXML.attrib["CarbonAPIVer"] = "1.2"
	cnpsXML.attrib["TaskType"]     = "JobCommand"
	
	
	JobCommand = Element("JobCommand")
	JobCommand.attrib["Command"] = command
	JobCommand.attrib["GUID"]    = guid

	if command == "SetPriority" and priority != None:
	    JobCommand.attrib["Priority.DWD"] = str(priority)

	cnpsXML.append(JobCommand)

	return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>' + tostring(cnpsXML, encoding="utf-8")

    else:
	return None


## FramesToCarbonFramesUnit(): Convert Frame in Carbon Frames Unit
#
# @param frames Frame, default = 0
# @param df     Is "DF" or "NDF", default "DF"
# @retval Carbon Frames Units
def FramesToCarbonFramesUnit(frames = 0, df = "DF"):
    if df == "DF":
        frameRate = 30000.0 / 1001.0
    elif df == "NDF":
        frameRate = 30
    else:
        return None

    carbonUnit = int(27000000 / frameRate)
    return (frames * carbonUnit)


def StichSource(FileSrc = []):
    
	i = 0

	Source = Element('Sources')

	for file in FileSrc:
	    Module         = Element('Module_%s' % str(i))
	    Module.attrib['Filename'] = file
	    Source.append(Module)
	    i = i + 1
	    
	dump(Source)    
	return Source


def ComplexSourceGetModule(module_id, streamType, srcTrack, dstTrack, filename):

        S_Module = Element("Module_"+str(module_id))
        S_Module.attrib["ElementaryStream"] = streamType
        S_Module.attrib["SourceTrack.DWD"] = str(srcTrack)
        S_Module.attrib["ComplexSourceTrack.DWD"] = str(dstTrack)
        S_Module.attrib["Filename"] = filename
        ret = S_Module

        return ret


def ComplexSourceGetSource(sourceList=[]):


        Source = Element("Sources")
        Module = Element("Module_0")
        Module.attrib["ComplexSource.DWD"] = "1"
        Module.attrib["Inpoint.QWD"]  ="-1"
	Source.append(Module)

        ModuleData = Element("ModuleData")

        i = 0

        for sl in sourceList:
                ModuleData.append(ComplexSourceGetModule(i, sl['type'], sl['srctrack'], sl['dsttrack'], sl['filename']))
                i = i + 1

        Module.append(ModuleData)
        ret = Source

        return ret


def MailNotify(PreTask=None, PostTask=None, TaskError=None):
	Notify = Element("Notify")
	
	if PreTask is not None:
		PreTaskNotify  = Element("PreTaskNotify")
		EmailNotifyPre = Element("EmailNotify_0")
                EmailNotifyPre.attrib["Subject"]   = PreTask['Subject']	
		EmailNotifyPre.attrib["Body"]	   = PreTask['Body']
		EmailNotifyPre.attrib["Recipient"] = PreTask['Recipient']
		PreTaskNotify.append(EmailNotifyPre)
		Notify.append(PreTaskNotify)


	if PostTask is not None:
                PostTaskNotify = Element("PostTaskNotify")
		EmailNotifyPost = Element("EmailNotify_0")
		EmailNotifyPost.attrib["Subject"]   = PostTask['Subject']
                EmailNotifyPost.attrib["Body"]      = PostTask['Body']
                EmailNotifyPost.attrib["Recipient"] = PostTask['Recipient']
		PostTaskNotify.append(EmailNotifyPost)
		Notify.append(PostTaskNotify)
		

	if TaskError is not None:
		TaskErrorNotify = Element("TaskErrorNotify")
		EmailNotifyError = Element("EmailNotify_0")
		EmailNotifyError.attrib["Subject"]   = TaskError['Subject']
                EmailNotifyError.attrib["Body"]      = TaskError['Body']
                EmailNotifyError.attrib["Recipient"] = TaskError['Recipient']
		TaskErrorNotify.append(EmailNotifyError)
		Notify.append(TaskErrorNotify)

	return Notify

	


## CreateCarbonXMLJob(): Generate a XML Carbon TaskType
#  
# @param s_path Source path of file
# @param s_filename Source filename
# @param s_cuttime List of dictionaries of timming [{in: "", out: ""}] in order
# @param d_lsit List of dictionaries [{d_guid: "", CML_P_BaseFileName: "", CML_P_Path: ""}]
# @retval OK: xml <cnpsXML TaskType="JobQueue"> or ERROR: None
def CreateCarbonXMLJob ( s_path="", s_filename="", s_cuttime=[], d_list = [], source=None, notify=None, stich=False ):
	
    # XML Default Header
    xmlheader = "<?xml version=\"1.0\"?>"
    
    if s_path == "" and s_filename == "" and len(d_list) == 0:
	print "Puto"
    	return None

	
    # TAG <cnpsXML CarbonAPIVer="" TaskType="">

    cnpsXML = Element("cnpsXML")
    cnpsXML.attrib["CarbonAPIVer"] ="1.2"
    cnpsXML.attrib["TaskType"] = "JobQueue"
    cnpsXML.attrib["Priority.DWD"] = "255"
    JobName = time.time() 
    cnpsXML.attrib["JobName"] = str(JobName)


    if notify is not None:
	cnpsXML.append(notify)	



    # TAG <Sources> Hijo de cnpsXML

    if source == None:
        Sources = Element("Sources")
    else:
	Sources = source	

    cnpsXML.append(Sources)

    # TAG <Module_0 Filename=""> Hijo de Sorces


    if source == None:
        S_Module = Element("Module_0")
        S_Module.attrib["Filename"] = s_path + s_filename

    # Si el tamanio de la lista de diccionatios de tiempos tiene elementos

        if len(s_cuttime) > 0:


	# TAG <InOutPoints Inpoint_n="" Outpoint_n=""> Hijo de Module_0
	    InOutPoints = Element("InOutPoints")

	    i = 0
	    for ctc in s_cuttime:
    	        instr = "Inpoint_" + str(i) + ".QWD"
	        outstr = "Outpoint_" + str(i) + ".QWD"
	        i = i + 1 
	        InOutPoints.attrib[instr] = str(ctc["in"]) 
	        InOutPoints.attrib[outstr] = str(ctc["out"])

	    S_Module.append(InOutPoints)

        Sources.append(S_Module)

    # TAG <Destinations> Hijo de cnpsXML

    Destinations = Element("Destinations")
	
    i = 0
    for dest in d_list:	
	modstr = "Module_" + str(i)
	i = i + 1
	# TAG <Module_n ModuleGUID=""> Hijo de Destinations		
	D_Module = Element(modstr)
	D_Module.attrib["ModuleGUID"] = dest["d_guid"]
	# TAG <ModuleData CML_P_BaseFileName="" CML_P_Data=""> Hijo de Module_n

	D_Module_Data = Element("ModuleData")
	D_Module_Data.attrib["CML_P_BaseFileName"] = dest["d_basename"]
	D_Module_Data.attrib["CML_P_Path"] = dest["d_path"]

	# Add start Timecode Filter

	Filter_0 = Element("Filter_0")
	
	j = 0
	
#	Filter_1 = Element("Filter_1") 
	if "subtitle" in dest:
		Module_Filter_SUB = Element("Module_%s" % j)
		j = j + 1
		Module_Filter_SUB.attrib["ModuleGUID"] = "{303EC062-9997-4975-9FED-228798D36687}"
		Module_Filter_SUB.attrib["PresetGUID"] = "{303EC062-9997-4975-9FED-228798D36687}"
		Module_Filter_Data = Element("ModuleData")		
		Module_Filter_Data.append(dest["subtitle"])
		Module_Filter_SUB.append(Module_Filter_Data)
		Filter_0.append(Module_Filter_SUB)

	if "logo" in dest:
		Module_Filter_SUB = Element("Module_%s" % j)
		j = j + 1
		Module_Filter_SUB.attrib["ModuleGUID"] = "{8D2AD32E-8B96-45E4-99F5-F9CC7E25A044}"
		Module_Filter_SUB.attrib["PresetGUID"] = "{8D2AD32E-8B96-45E4-99F5-F9CC7E25A044}"
		Module_Filter_SUB.append(dest['logo'])
		Filter_0.append(Module_Filter_SUB)


	if "d_start_tc" in dest:
		Module_Filter = Element("Module_%s" % j)
		j = j + 1
		Module_Filter.attrib["ModuleGUID"] = "{3DF7826F-04DC-48FD-A338-3BC706C5B4D4}"
		Module_Filter.attrib["PresetGUID"] = "{3DF7826F-04DC-48FD-A338-3BC706C5B4D4}"
		Module_Filter.attrib["Mode.DWD"]   = "0"
		Module_Filter.attrib["Source.DWD"] = "2"
		Module_Filter.attrib["TCOffset"]   = "00:00:00"
		Module_Filter.attrib["TCStart"]	   = "01:00:00:00"
		Module_Filter.attrib["DropFrame.DWD"] = "1"
		Module_Filter_Data = Element("ModuleData")
		Module_Filter_Data.attrib["StartTC"] = dest["d_start_tc"]
		Module_Filter.append(Module_Filter_Data)
		Filter_0.append(Module_Filter)
    
	D_Module.append(Filter_0)
	D_Module.append(D_Module_Data)

	Destinations.append(D_Module)

    cnpsXML.append(Destinations)
    if stich == True:
	ProjectSettings = Element('ProjectSettings')
	ProjectSettings.attrib['Stitching.DWD'] = "1"
	cnpsXML.append(ProjectSettings)
		
    print tostring(cnpsXML, encoding="utf-8") 
    return xmlheader + tostring(cnpsXML, encoding="utf-8")       


