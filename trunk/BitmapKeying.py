from xml.etree.ElementTree import *


class BitmapKeying(object):
    def __init__(self):
	self.Filename      = ''
	self.Dialog_BIN    = ''
	self.Position_DWD  = ''
	self.Scale_DBL     = ''
	self.Offset_DBL    = ''
	self.Opacity_DBL   = ''
    
    
    def ToElement(self):
	ModuleData = Element('ModuleData')
	ModuleData.attrib['Filename']    = self.Filename
	ModuleData.attrib['Dialog.BIN']  = self.Dialog_BIN 
	ModuleData.attrib['Position.DWD']= self.Position_DWD
	ModuleData.attrib['Scale.DBL']   = self.Scale_DBL
	ModuleData.attrib['Offset.DBL']  = self.Offset_DBL
	ModuleData.attrib['Opacity.DBL'] = self.Opacity_DBL
	return ModuleData
	
	