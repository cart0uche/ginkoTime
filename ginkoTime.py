# -*- coding: utf-8 -*-
# ginkoTime

import os
import ConfigParser
import requests
import wx
from BeautifulSoup import BeautifulSoup
import json


GINKO_URL = "http://www.ginkobus.com/templates/tribu/lib/get_tempo.php"


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
		if (self.proxy_enable == 1):
			self.proxy = {
						"http": "http://" + config.get('proxy', 'login') + ":"
						+ config.get('proxy', 'password') + "@"
						+ config.get('proxy', 'url')
			}
		else:
			self.proxy = None

	def loadLines(self):
		json_data = open('lines.json').read()
		self.lines = json.loads(json_data)
		print self.lines

	def CreatePopupResult(self, evt=None):
		menu = wx.Menu()
		menu.Append(-1, "GinkoTime")

		for i, line in enumerate(self.lines["lines"]):
			menu.AppendSeparator()
			scheduleList = self.getSchedule(line["stop"], line["line"], line["direction"])
			menu.Append(-1, "Ligne " + line["line"] + " - Arret " + line["stop"])
			for schedule in scheduleList:
				if schedule is not u'':
					menu.Append(-1, schedule)
		return menu

	def getSchedule(self, stop, line, direction):
		print "stop=" + stop + " line=" + line + " direction=" + direction
		scheduleList = []
		params = {'ligne': line, 'arret': stop, 'type': '3'}
		page_html = requests.post(GINKO_URL, data=params, proxies=self.proxy)
		soup = BeautifulSoup(page_html.text)
		td1 = soup.findAll('td')
		for i, X in enumerate(td1):
			if (X.text == line):
				print X.text + " found"
				currentDirection = td1[i+1]
				if (currentDirection.text == direction):
					print direction + " found"
					schedule1 = td1[i+2]
					schedule2 = td1[i+3]
					scheduleList.append(schedule1.text)
					scheduleList.append(schedule2.text)
					break
		print scheduleList
		return scheduleList

	def CreatePopupMenu(self, evt=None):
		menu = wx.Menu()
		menu.AppendSeparator()
		menu.Append(self.TBMENU_CLOSE, "Exit Program")
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

###########################################################################


def main():
	app = wx.App(False)
	GinkoTime()
	app.MainLoop()

if __name__ == '__main__':
	main()
