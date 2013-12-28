#!/usr/bin/python

import sys
from PyQt4 import QtGui, QtCore, Qt

name = 'ZaPF-Jeopardy (v0.1)'

class Jeopardy(QtGui.QWidget):

	def quit(self):
		self.app.quit()


	def select_field(self,category_id,level):
		print('category: '+str(category_id)+' at level '+str(level))
		self.set_response(True)


	def correct(self):
		print('CORRECT!')
		self.set_response(False)


	def wrong(self):
		print('WRONG!')
		self.set_response(False)


	def reopen(self):
		print('REOPEN')
		self.set_response(False)


	def set_response(self,a):
		self.correct_button.setEnabled(a)
		self.wrong_button.setEnabled(a)
		self.reopen_button.setEnabled(a)
		
		for i in self.jeopardy_button:
			for j in i:
				j.setDisabled(a)


	def __init__(self,app):
		super(Jeopardy,self).__init__()
		print(name)
		self.app = app

		self.grid = QtGui.QGridLayout(self)

		# Create the Jeopardy window
		jeopardy_window = QtGui.QHBoxLayout(self)
		jeopardy_category_layouts = []
		jeopardy_categories = ['test1','test2','test3','test4','test5']
		self.jeopardy_category_label = []

		# Create the Jeopardy buttons
		self.jeopardy_button = []
		for i in range(5):
			jeopardy_category_layouts.append(QtGui.QVBoxLayout(self))
			self.jeopardy_category_label.append(QtGui.QLabel(jeopardy_categories[i]))
			#self.jeopardy_category_label[i].setMargin(10)
			jeopardy_category_layouts[i].addWidget(self.jeopardy_category_label[i])
			self.jeopardy_button.append([])
			
			for j in range(5):
				self.jeopardy_button[i].append(QtGui.QPushButton(str(j+1)))
				self.jeopardy_button[i][j].setSizePolicy(QtGui.QSizePolicy.Ignored,QtGui.QSizePolicy.Ignored)
				jeopardy_category_layouts[i].addWidget(self.jeopardy_button[i][j])
				self.app.connect(self.jeopardy_button[i][j],Qt.SIGNAL('pressed()'),lambda i=[i,j]: self.select_field(i[0],i[1]))
			jeopardy_window.addLayout(jeopardy_category_layouts[i])

		# Create the Answer section
		answer_section_layout = QtGui.QHBoxLayout(self)

		answer_label = QtGui.QLabel('Answer')
		answer_section_layout.addWidget(answer_label)

		# Create the Repsonse section
		response_section_layout = QtGui.QVBoxLayout(self)
		self.correct_button = QtGui.QPushButton('CORRECT')
		self.wrong_button = QtGui.QPushButton('WRONG')
		self.reopen_button = QtGui.QPushButton('REOPEN')
		self.set_response(False)

		response_section_layout.addWidget(self.correct_button)
		response_section_layout.addWidget(self.wrong_button)
		response_section_layout.addWidget(self.reopen_button)

		# Create the Player section
		player_section_layout = QtGui.QVBoxLayout(self)

		player_label = QtGui.QLabel('Player')
		player_section_layout.addWidget(player_label)

		# Create the Global Butten section
		global_button_layout = QtGui.QVBoxLayout(self)

		quit = QtGui.QPushButton('quit')
		quit.setFixedHeight(50)
		global_button_layout.addWidget(quit)

		# Add everything to the grid
		self.grid.addLayout(jeopardy_window,0,0,4,4)
		self.grid.addLayout(answer_section_layout,5,1,1,3)
		self.grid.addLayout(player_section_layout,0,5,4,1)
		self.grid.addLayout(global_button_layout,5,5)
		self.grid.addLayout(response_section_layout,5,0)

		# Connecitong buttons to functions
		self.app.connect(quit,Qt.SIGNAL('pressed()'),lambda: self.quit())
		self.app.connect(self.correct_button,Qt.SIGNAL('pressed()'),lambda: self.correct())
		self.app.connect(self.wrong_button,Qt.SIGNAL('pressed()'),lambda: self.wrong())
		self.app.connect(self.reopen_button,Qt.SIGNAL('pressed()'),lambda: self.reopen())

		self.setLayout(self.grid)
		self.setWindowTitle(name)
		self.show()
#		self.showMaximized()

def main():
	app = QtGui.QApplication(sys.argv)
	jeopardy = Jeopardy(app)
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
