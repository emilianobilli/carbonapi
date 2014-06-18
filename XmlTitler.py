from xml.etree.ElementTree import *

class TitlerData(object):
    def __init__(self):
	self.Data = []

    def AppendData(self, Data):
	self.Data.append(Data)

    def ToElement(self):
	TitleData = Element('TitlerData')
	for data in self.Data:
	    TitleData.append(data.ToElement())
	return TitleData

class Data(object):
    def __init__(self):
	self.Font		= ''
	self.FontCharSet	= ''
	self.StartTimecode	= ''
	self.EndTimecode  	= ''
	self.Title		= ''
	self.CharSize		= ''
	self.PosX		= ''
	self.PosY		= ''
	self.ColorR		= ''
	self.ColorG		= ''
	self.ColorB		= ''
	self.Transparency	= ''
	self.ShadowSize		= ''
	self.HardShadow		= ''
	self.BkgEnable		= ''
	self.BkgSemiTransparent = ''
	self.BkgExtraWidth	= ''
	self.BkgExtraHeight	= ''
	self.RightToLeft	= ''
	self.HAlign		= ''
	self.VAlign		= ''

    def ToElement(self):
	Data = Element('Data')
	Data.attrib['Title']		= self.Title
	Data.attrib['StartTimecode']	= self.StartTimecode
	Data.attrib['EndTimecode']	= self.EndTimecode

	if self.Font != '':
	    Data.attrib['Font']		= self.Font    
	if self.FontCharSet != '':
	    Data.attrib['FontCharSet']	= self.FontCharSet
	if self.CharSize != '':
	    Data.attrib['CharSize']	= self.CharSize
	if self.PosX != '':
	    Data.attrib['PosX']		= self.PosX
	if self.PosY != '':
	    Data.attrib['PosY']		= self.PosY
	if self.ColorR != '':
	    Data.attrib['ColorR']	= self.ColorR
	if self.ColorG != '':
	    Data.attrib['ColorG']	= self.ColorG
	if self.ColorB != '':
	    Data.attrib['ColorB']	= self.ColorB
	if self.Transparency != '':
	    Data.attrib['Transparency'] = self.Transparency
	if self.ShadowSize != '':
	    Data.attrib['ShadowSize']	= self.ShadowSize
	if self.HardShadow != '':
	    Data.attrib['HardShadow']	= self.HardShadow
	if self.BkgEnable  != '':
	    Data.attrib['BkgEnable']	= self.BkgEnable
	if self.BkgSemiTransparent != '':
	    Data.attrib['BkgSemiTransparent'] = self.BkgSemiTransparent
	if self.BkgExtraWidth != '':
	    Data.attrib['BkgExtraWidth'] = self.BkgExtraWidth
	if self.BkgExtraHeight != '':
	    Data.attrib['BkgExtraHeight'] = self.BkgExtraHeight
	if self.RightToLeft != '':
	    Data.attrib['RightToLeft']	= self.RightToLeft
	if self.HAlign != '':
	    Data.attrib['HAlign']	= self.HAlign
	if self.VAlign != '':
	    Data.attrib['VAlign']	= self.VAlign
    
	return Data


