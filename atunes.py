#!/usr/bin/python

from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys, os, subprocess, re
 
class MainWindow(QMainWindow):
	
	def __init__(self):
		
		QMainWindow.__init__(self)
		self.ui = uic.loadUi("main.ui", self)
		self.connect_wiring()
		
		# The subprocess to play the sound
		# TODO create a hash table for the players
		# since there won't be one single player
		#self.player = None
		
		self.last_line_id = 1
				
	def connect_wiring(self):
		
		self.add_line.clicked.connect(self.handle_add_clicked)
		self.remove_1.clicked.connect(self.handle_remove_clicked)
		
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
		self.scrollAreaWidgetContents.layout().addWidget(edit, rows+1, 2)
		
		remove = QPushButton(self.ui.scrollAreaWidgetContents)
		remove.setObjectName("remove_" + str(self.last_line_id))
		remove.setText("Remove")
		self.scrollAreaWidgetContents.layout().addWidget(remove, rows+1, 3)

		play = QPushButton(self.ui.scrollAreaWidgetContents)
		play.setObjectName("play_" + str(self.last_line_id))
		play.setText("Play")
		self.scrollAreaWidgetContents.layout().addWidget(play, rows+1, 4)	
		
	
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

