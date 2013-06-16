# -*- coding: utf-8 -*-
# ginkoTime

import os
import ConfigParser
import urllib
import urllib2
import wx
from BeautifulSoup import BeautifulSoup
import json


GINKO_URL = 'www.ginkobus.com/templates/tribu/lib/get_tempo.php'


class GinkoTime(wx.TaskBarIcon):

	TBMENU_CLOSE = wx.NewId()

	def __init__(self):
		self.loadConfig()
		self.loadLines()

		wx.TaskBarIcon.__init__(self)
		self.tbIcon = wx.Icon('icon.png', wx.BITMAP_TYPE_PNG)
		self.SetIcon(self.tbIcon, 'GinkoTime')

		self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)
		self.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.OnTaskBarRightClick)
		self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.TBMENU_CLOSE)

	def loadConfig(self):
		config = ConfigParser.SafeConfigParser()
		if os.path.isfile('ginko.ini'):
			config.read('ginko.ini')

		self.proxy_enable = config.get('proxy', 'enable')
		self.proxy_login = config.get('proxy', 'login')
		self.proxy_password = config.get('proxy', 'password')

	def loadLines(self):
		json_data = open('lines.json').read()
		self.lines = json.loads(json_data)
		print self.lines

	def CreatePopupMenu(self, evt=None):
		menu = wx.Menu()
		menu.AppendSeparator()
		menu.Append(self.TBMENU_CLOSE, "Exit Program")
		return menu

	def CreatePopupResult(self, evt=None):
		if (self.proxy_enable == 1):
			url = 'http://' + self.login + ':' + self.proxy_password + '@' + GINKO_URL
		else:
			url = 'http://' + GINKO_URL

		menu = wx.Menu()
		menu.Append(-1, "GinkoTime")

		for i in range(len(self.lines["lines"])):
			menu.AppendSeparator()
			scheduleList = self.getSchedule(url, self.lines["lines"][i]["stop"], self.lines["lines"][i]["line"], self.lines["lines"][i]["direction"])
			menu.Append(-1, "Ligne " + self.lines["lines"][i]["line"] + " - Arret " + self.lines["lines"][i]["stop"])
			for schedule in scheduleList:
				menu.Append(-1, schedule)
		return menu

	def OnTaskBarLeftClick(self, event):
		menu = self.CreatePopupResult()
		self.PopupMenu(menu)
		menu.Destroy()

	def OnTaskBarRightClick(self, event):
		menu = self.CreatePopupMenu()
		self.PopupMenu(menu)
		menu.Destroy()

	def OnTaskBarClose(self, event):
		self.RemoveIcon()
		self.Destroy()

	def getSchedule(self, url, stop, line, direction):
		print "getSchedule for stop " + stop + " line " + line + " direction " + direction
		scheduleList = []
		params = urllib.urlencode({'type': '3', 'arret': stop, 'ligne': line})
		request = urllib2.Request(url, params)
		response = urllib2.urlopen(request)
		page_html = response.read()
		# print page_html
		soup = BeautifulSoup(page_html)
		td1 = soup.findAll('td')
		for i, X in enumerate(td1):
			if (X.text == line):
				currentDirection = td1[i+1]
				if (currentDirection.text == direction):
					schedule1 = td1[i+2]
					schedule2 = td1[i+3]
					if not schedule1:
						scheduleList.append(schedule1.text)
					if not schedule2:
						scheduleList.append(schedule2.text)
					break
		print scheduleList
		return scheduleList


###########################################################################


def main():
	app = wx.App(False)
	GinkoTime()
	app.MainLoop()

if __name__ == '__main__':
	main()
