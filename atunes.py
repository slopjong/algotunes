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
		# TODO: use one signal mapper per button type (remove, import, play, ...)
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
		
		# 
		self.map_text_changed_signals()
				
		# import presets from the patte.rn file
		f = open('patte.rn', "r")
		patterns = f.readlines()
		f.close()
		for pattern in patterns:
			pattern = pattern.rstrip('\r\n')
			self.presets.addItem(pattern)
		
		# connect the preset list
		self.presets.itemDoubleClicked.connect(self.preset_clicked)
		
		self.objects = {'edit_1': self.ui.edit_1, 'import_1':self.ui.import_1, 'remove_1': self.ui.remove_1, 'play_stop_1': self.ui.play_stop_1}
		self.players = {}
		
		# creating the temp folder for the samples
		os.system("mkdir -p /tmp/algotunes")
		
	def map_text_changed_signals(self):
		
		self.text_changed_mapper = QSignalMapper(self)
		self.text_changed_mapper.setMapping(self.edit_1, 1)
		self.connect(self.edit_1, SIGNAL("textEdited(QString)"), self.text_changed_mapper, SLOT("map()"))
		self.connect( self.text_changed_mapper, SIGNAL("mapped(int)"), self.text_changed)

	# activates the import button as soon as the line edit contains a pattern which is not yet in the list
	def text_changed(self, line_number):
		
		edit_text = self.objects["edit_" + str(line_number)].text()
		list = self.presets.findItems(edit_text, Qt.MatchExactly)
		
		button = self.objects["import_" + str(line_number)]
		if(len(list) == 0):
			button.setEnabled(True)
		else:
			button.setEnabled(False)
		
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

		# delete the import button
		_import = self.objects["import_" + line_number]
		_import .setParent(None)
		del self.objects["import_" + line_number]
		
		# delete the play/stop button
		play = self.objects["play_stop_" + line_number]
		play.setParent(None)
		del self.objects["play_stop_" + line_number]
		
		player = self.players.get("player_" + line_number)
		
		if(player != None):
			self.stop(player, line_number)

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

		# listen to text edited events
		self.connect(edit, SIGNAL("textEdited(QString)"), self.text_changed_mapper, SLOT("map()"))
		self.text_changed_mapper.setMapping(edit, self.last_line_id)
		
		_import = QPushButton(self.ui.scrollAreaWidgetContents)
		_import.setObjectName("import_" + str(self.last_line_id))
		_import.setText("Import")
		_import.setEnabled(False)
		self.scrollAreaWidgetContents.layout().addWidget(_import, rows+1, 1)	
		
		#self.connect(_import, SIGNAL("clicked()"), self.import_clicked_mapper, SLOT("map()"))
		#self.signal_mapper.setMapping(_import, self.last_line_id)
		
		remove = QPushButton(self.ui.scrollAreaWidgetContents)
		remove.setObjectName("remove_" + str(self.last_line_id))
		remove.setText("Remove")
		self.scrollAreaWidgetContents.layout().addWidget(remove, rows+1, 2)

		self.connect(remove, SIGNAL("clicked()"), self.signal_mapper, SLOT("map()"))
		self.signal_mapper.setMapping(remove, "remove_" + str(self.last_line_id))
		
		play = QPushButton(self.ui.scrollAreaWidgetContents)
		play.setObjectName("play_" + str(self.last_line_id))
		play.setText("Play")
		self.scrollAreaWidgetContents.layout().addWidget(play, rows+1, 3)	
		
		self.connect(play, SIGNAL("clicked()"), self.signal_mapper, SLOT("map()"))
		self.signal_mapper.setMapping(play, "play_stop_" + str(self.last_line_id))
	
		# add the new components to the objects dictionary
		self.objects["edit_" + str(self.last_line_id)] = edit
		self.objects["import_" + str(self.last_line_id)] = _import
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
		player = Popen(["aplay", "-r8000"], stdin=p3.stdout)
		
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