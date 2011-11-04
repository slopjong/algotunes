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
        self.player = None
        self.edits = [self.edit_1]
        self.last_edit_id = 1
	
    def connect_wiring(self):
        self.play_stop_btn.clicked.connect(self.handle_play_stop_clicked)
        self.add_btn.clicked.connect(self.handle_add_clicked)
        self.remove_btn.clicked.connect(self.handle_remove_clicked)
	
    def handle_play_stop_clicked(self):
        if self.play_stop_btn.text() == "Play":
            self.write()
            self.compile_file()
            self.play()
            self.play_stop_btn.setText("Stop")
        else:
            self.stop()
            self.play_stop_btn.setText("Play")
	    
    def handle_add_clicked(self):
        edit = QLineEdit(self.ui.scrollAreaWidgetContents)
        self.last_edit_id += 1
        edit.setObjectName("edit_" + str(self.last_edit_id))
        self.scrollAreaWidgetContents.layout().addWidget(edit)
        self.edits.append(edit)
	
    def handle_remove_clicked(self):
        if len(self.edits) <= 1:
            return
        children = self.scrollAreaWidgetContents.children()
        last = None
        for c in children:
            if re.match("edit_\d+", c.objectName()) != None:
                last = c
        self.scrollAreaWidgetContents.layout().removeWidget(last)
        self.edits.remove(last)
        last.setParent(None)
	
    def write(self):
        writer = open(self.output_edit.text() + ".c", "w")
        writer.write("#include <stdio.h>\n")
        writer.write("int main() {\n")
        writer.write("\t" + self.loop_edit.text() + " {\n")
        writer.write("\t\tputchar(\n")
        write_edits = []
        for edit in self.edits:
            if edit.text() != "":
                write_edits.append(edit)
        for idx in range(0, len(write_edits)):
            writer.write("\t\t(t%" + str(len(write_edits)) + "==" + str(idx) + "?" + write_edits[idx].text() + ":\n")
        writer.write("0")
        for idx in range(0, len(write_edits)+1): #+1 for the putchar( parenthesis
            writer.write(")")
        writer.write(";\n}\n}")
        writer.close()
	
    def compile_file(self):
        if os.system("gcc %(file)s.c -std=c99 -o%(file)s.out" % { "file":self.output_edit.text() }) != 0:
            QMessageBox.critical(self, "Error", "Compilation failed")
	    
    def play(self):
        if self.player != None:
            self.stop()
        self.source = subprocess.Popen("./%s.out" % self.output_edit.text(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #self.player = subprocess.Popen(["pacat", "--format", "u8", "--rate", "8000"], stdin=self.source.stdout)
        self.player = subprocess.Popen(["aplay"], stdin=self.source.stdout)
	
    def stop(self):
        if self.player == None:
            return
        self.player.terminate()
        self.player = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = MainWindow()
    wnd.show()
    app.exec_()

