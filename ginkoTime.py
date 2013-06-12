#!/usr/bin/python
# -*- coding: utf-8 -*-
# ginkoTime

import os
import ConfigParser
import urllib,urllib2
import wx
from BeautifulSoup import BeautifulSoup   

GINKO_URL = 'www.ginkobus.com/templates/tribu/lib/get_tempo.php'


class GinkoTime(wx.TaskBarIcon):

	TBMENU_CLOSE = wx.NewId()

	def __init__(self):
		self.loadConfig()

		wx.TaskBarIcon.__init__(self)
		self.tbIcon=wx.Icon('icon.png',wx.BITMAP_TYPE_PNG)
		self.SetIcon(self.tbIcon, 'GinkoOnTime')

		self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)
		self.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.OnTaskBarRightClick)
		self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.TBMENU_CLOSE)


	def loadConfig(self):
		config = ConfigParser.SafeConfigParser()
		if os.path.isfile('ginko.ini'):
			config.read('ginko.ini')

		self.__stop  = config.get('config','stop')
		self.__line = config.get('config','line')
		self.__direction = config.get('config','direction')

		self.__proxy_enable = config.get('proxy','enable')
		self.__proxy_login = config.get('proxy','login')
		self.__proxy_password = config.get('proxy','password')


	def CreatePopupMenu(self, evt=None):
		menu=wx.Menu()
		menu.AppendSeparator()
		menu.Append(self.TBMENU_CLOSE, "Exit Program")
		return menu


	def CreatePopupResult(self, evt=None):
		if (self.__proxy_enable==1):
			url = 'http://' + self.__login + ':' + self.__proxy_password + '@' + GINKO_URL
		else:
			url = 'http://' + GINKO_URL	

		scheduleList = self.getSchedule(url,self.__stop,self.__line,self.__direction)

		menu=wx.Menu()
		menu.Append(-1,"GinkoTime")
		menu.AppendSeparator()
		menu.Append(-1,"Ligne " +  self.__line + " - Arret " + self.__stop)
		for schedule in scheduleList:
			menu.Append(-1, schedule)
		return menu

	def OnTaskBarLeftClick(self,event):
		menu = self.CreatePopupResult()
		self.PopupMenu(menu)
		menu.Destroy()

	def OnTaskBarRightClick(self,event):
		menu = self.CreatePopupMenu()
		self.PopupMenu(menu)
		menu.Destroy()

	def OnTaskBarClose(self,event):
		self.RemoveIcon()
		self.Destroy()

	def getSchedule(self, url, stop, line,direction):
		scheduleList = []
		params = urllib.urlencode({'type':'3', 'arret':stop,'ligne':line})
		request = urllib2.Request(url,params)
		response= urllib2.urlopen(request)
		page_html = response.read()
		# print page_html
		soup =  BeautifulSoup(page_html)
		td1 = soup.findAll('td')
		for i,X in enumerate(td1):
			if (X.text==line):
				currentDirection = td1[i+1]
				if (currentDirection.text==direction):
					schedule1 = td1[i+2]
					schedule2 = td1[i+3]
					scheduleList.append(schedule1.text)
					scheduleList.append(schedule2.text)
					break
		return scheduleList

###########################################################################

def main():
	app = wx.App(False)
	taskBarIcon = GinkoTime()
	app.MainLoop()

if __name__ == '__main__':
	main()
