#!/usr/bin/python

from PyQt4 import uic

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from subprocess import *

import sys, os, re

 
class MainWindow(QMainWindow):
	
	def __init__(self):
		
		# initialize the user interface
		QMainWindow.__init__(self)
		self.ui = uic.loadUi("main.ui", self)

		# define a signal mapper to map fired signals of a series of buttons to one single handler
		# for code examples, see [1] and [2]
		self.signal_mapper = QSignalMapper(self)
		self.connect(self.signal_mapper, SIGNAL("mapped(const QString &)"), self.button_clicked)

		# connect the initial existing remove button of the first line with the signal mapper
		self.connect(self.remove_1, SIGNAL("clicked()"), self.signal_mapper, SLOT("map()"))
		self.signal_mapper.setMapping(self.remove_1, "remove_1")

		# connect the initial existing play/stop button of the first line with the signal mapper
		self.connect(self.play_stop_1, SIGNAL("clicked()"), self.signal_mapper, SLOT("map()"))
		self.signal_mapper.setMapping(self.play_stop_1, "play_stop_1")
		
		# an ID which is incremented each time a new line is added
		self.last_line_id = 1	
		
		# button to add a new line
		self.add_line.clicked.connect(self.handle_add_clicked)
		
		# connect the preset list
		self.presets.itemDoubleClicked.connect(self.preset_clicked)
		
		self.objects = {'edit_1': self.ui.edit_1, 'remove_1': self.ui.remove_1, 'play_stop_1': self.ui.play_stop_1}
		self.players = {}
		
		# creating the temp folder for the samples
		os.system("mkdir -p /tmp/algotunes")
		
	# See [0]
	def closeEvent(self, event):
		os.system("rm -rf /tmp/algotunes")
		os.system("killall aplay")
		event.accept()

		
	def button_clicked(self, action):
		
		m = re.search('\d+', action)
		line_number = m.group(0)

		m = re.search('remove', action)
		if(m!=None):
			self.delete_line(line_number)

		m = re.search('play_stop', action)
		if(m!=None):
			self.handle_play_stop_clicked(line_number)

	def delete_line(self, line_number):

		# delete the edit field
		edit = self.objects["edit_" + line_number]
		edit.setParent(None)
		del self.objects["edit_" + line_number]
		
		# delete the remove button
		remove = self.objects["remove_" + line_number]
		remove.setParent(None)
		del self.objects["remove_" + line_number]
		
		# delete the play/stop button
		play = self.objects["play_stop_" + line_number]
		play.setParent(None)
		del self.objects["play_stop_" + line_number]
			
	def handle_play_stop_clicked(self, line_number):
		
		player = self.players.get("player_" + line_number)
		
		if(player == None):
			self.play(line_number)
		else:
			self.stop(player, line_number)
		
	def handle_add_clicked(self):
		
		self.last_line_id += 1
		rows = self.ui.scrollAreaWidgetContents.layout().rowCount()
		
		edit = QLineEdit(self.ui.scrollAreaWidgetContents)
		edit.setObjectName("edit_" + str(self.last_line_id))
		self.scrollAreaWidgetContents.layout().addWidget(edit, rows+1, 0)
		
		remove = QPushButton(self.ui.scrollAreaWidgetContents)
		remove.setObjectName("remove_" + str(self.last_line_id))
		remove.setText("Remove")
		self.scrollAreaWidgetContents.layout().addWidget(remove, rows+1, 1)

		self.connect(remove, SIGNAL("clicked()"), self.signal_mapper, SLOT("map()"))
		self.signal_mapper.setMapping(remove, "remove_" + str(self.last_line_id))
		
		play = QPushButton(self.ui.scrollAreaWidgetContents)
		play.setObjectName("play_" + str(self.last_line_id))
		play.setText("Play")
		self.scrollAreaWidgetContents.layout().addWidget(play, rows+1, 2)	
		
		self.connect(play, SIGNAL("clicked()"), self.signal_mapper, SLOT("map()"))
		self.signal_mapper.setMapping(play, "play_stop_" + str(self.last_line_id))
	
		# add the new components to the objects dictionary
		self.objects["edit_" + str(self.last_line_id)] = edit
		self.objects["remove_" + str(self.last_line_id)] = remove
		self.objects["play_stop_" + str(self.last_line_id)] = play
		
	def preset_clicked(self, item):
		
		self.handle_add_clicked()
		edit = self.objects["edit_" + str(self.last_line_id)]
		edit.setText(item.text())
		
	def play(self, line_number):

		# for Popen and os.system stuff, see [3] and [4]
		sample = self.objects["edit_" + line_number].text()
		
		p1 = Popen(["echo", "main(t){for(t=0;;++t)putchar("+ sample +");}"], stdout=PIPE)
		p2 = Popen(["gcc", "-xc", "-lm", "-o/tmp/algotunes/" + line_number + ".8b", "-"], stdin=p1.stdout)
		
		# wait until the sample is compiled
		p2.wait()
		
		p3 = Popen(["/tmp/algotunes/" + line_number + ".8b" ], stdout=PIPE)
		player = Popen(["aplay"], stdin=p3.stdout)
		
		self.players["player_" + line_number] = player
		self.objects["play_stop_" + line_number].setText("Stop")
	
	def stop(self, player, line_number):
		
		# reset the text to play
		self.objects["play_stop_" + line_number].setText("Play")
		
		# stop the player and remove it from the list
		player.terminate()
		del self.players["player_" + line_number]

if __name__ == "__main__":
	app = QApplication(sys.argv)
	wnd = MainWindow()
	wnd.show()
	app.exec_()


######################################################################
# [0] http://stackoverflow.com/questions/1414781/prompt-on-exit-in-pyqt-application
# [1] http://diotavelli.net/PyQtWiki/Using%20a%20signal%20mapper
# [2] http://pysnippet.blogspot.com/2010/06/qsignalmapper-at-your-service.html
# [3] http://www.python.org/dev/peps/pep-0324/
# [4] http://stackoverflow.com/questions/4813238/difference-between-subprocess-popen-and-os-system
######################################################################