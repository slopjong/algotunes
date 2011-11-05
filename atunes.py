#!/usr/bin/python

from PyQt4 import uic

from PyQt4.QtGui import *
from PyQt4.QtCore import *

#from PyQt4.QtGui import QApplication, QMainWindow, QPushButton, QLineEdit
#from PyQt4.QtCore import QSignalMapper, pyqtSignal

import sys, os, subprocess, re
 
class MainWindow(QMainWindow):
	
	def __init__(self):
		
		# initialize the user interface
		QMainWindow.__init__(self)
		self.ui = uic.loadUi("main.ui", self)
		

		# Some code examples for a signal mapper here:
		# 
		#    * http://diotavelli.net/PyQtWiki/Using%20a%20signal%20mapper
		#    * http://pysnippet.blogspot.com/2010/06/qsignalmapper-at-your-service.html
		#
		# define a signal mapper to map fired signals of a series of buttons to one single handler
		self.signal_mapper = QSignalMapper(self)
		self.connect(self.signal_mapper, SIGNAL("mapped(const QString &)"), self.button_clicked)

		# connect the initial existing remove button of the first line with the signal mapper
		self.connect(self.remove_1, SIGNAL("clicked()"), self.signal_mapper, SLOT("map()"))
		self.signal_mapper.setMapping(self.remove_1, "remove_1")

		# connect the initial existing play/stop button of the first line with the signal mapper
		self.connect(self.play_stop_1, SIGNAL("clicked()"), self.signal_mapper, SLOT("map()"))
		self.signal_mapper.setMapping(self.play_stop_1, "play_stop_1")
		
		# The subprocess to play the sound
		# TODO create a hash table for the players
		# since there won't be one single player
		#self.player = None
		
		# an ID which is incremented each time a new line is added
		self.last_line_id = 1	
		
		# button to add a new line
		self.add_line.clicked.connect(self.handle_add_clicked)
		
	def button_clicked(self, action):
		
		m = re.search('\d', action)
		line_numer = m.group(0)

		m = re.search('remove', action)
		if(m!=None):
			print(self.remove_1)

		m = re.search('play_stop', action)
		if(m!=None):
			print("play_stop")
		
	def handle_play_stop_clicked(self):
		
		#if self.play_stop_btn.text() == "Play":
		#	self.write()
		#	self.compile_file()
		#			self.play()
		#	self.play_stop_btn.setText("Stop")
		#else:
		#	self.stop()
		#	self.play_stop_btn.setText("Play")
		print("handle_play_stop_clicked")
		
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
	
	def handle_remove_clicked(self):
		
		print("handle_remove_clicked")
	
	
	def compile_file(self):
		
		#if os.system("gcc %(file)s.c -std=c99 -o%(file)s.out" % { "file":self.output_edit.text() }) != 0:
		#	QMessageBox.critical(self, "Error", "Compilation failed")
		print("compile")
		
	def play(self):
		
		#if self.player != None:
		#	self.stop()
		#self.source = subprocess.Popen("./%s.out" % self.output_edit.text(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		#self.player = subprocess.Popen(["pacat", "--format", "u8", "--rate", "8000"], stdin=self.source.stdout)
		#self.player = subprocess.Popen(["aplay"], stdin=self.source.stdout)
		print("play")
	
	def stop(self):
		
		#if self.player == None:
		#	return
		#self.player.terminate()
		#self.player = None
		print("stop")

if __name__ == "__main__":
	app = QApplication(sys.argv)
	wnd = MainWindow()
	wnd.show()
	app.exec_()

