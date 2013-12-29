#!/usr/bin/python

import sys
from PyQt4 import QtGui, QtCore, Qt

name = 'ZaPF-Jeopardy (v0.1)'

class Jeopardy(QtGui.QWidget):

	class Player:

		def __init__(self):
			self.name = 'foobar'
			self.punket = 0


	def quit(self):
		self.app.quit()


	def select_field(self,category_id,level):
		print('category: '+str(category_id)+' at level '+str(level))
		self.current_field = [category_id,level]
		self.jeopardy_button[category_id][level].setPalette(QtGui.QPalette(QtGui.QColor(255,255,255)))
		self.listen = True
		self.set_field_activity(False)


	def correct(self):
		print('CORRECT!')
		self.set_response(False)
		self.set_field_activity(True)
		#print(self.jeopardy_button


	def wrong(self):
		print('WRONG!')
		self.jeopardy_button[self.current_field[0]][self.current_field[1]].setPalette(self.palette())
		self.set_response(False)
		self.set_field_activity(True)


	def reopen(self):
		print('REOPEN')
		self.jeopardy_button[self.current_field[0]][self.current_field[1]].setPalette(self.palette())
		self.set_response(False)
		self.set_field_activity(True)


	def player_pressed(self,player_id):
		if self.listen:
			print(player_id)
			self.listen = False
			self.set_response(True)


	def set_response(self,a):
		self.correct_button.setEnabled(a)
		self.wrong_button.setEnabled(a)
		self.reopen_button.setEnabled(a)
		

	def set_field_activity(self,a):
		for i in self.jeopardy_button:
			for j in i:
				j.setEnabled(a)


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
		self.correct_button.setPalette(QtGui.QPalette(QtGui.QColor(0,255,0)))
		self.wrong_button = QtGui.QPushButton('WRONG')
		self.wrong_button.setPalette(QtGui.QPalette(QtGui.QColor(255,0,0)))
		self.reopen_button = QtGui.QPushButton('REOPEN')
		self.set_response(False)

		response_section_layout.addWidget(self.correct_button)
		response_section_layout.addWidget(self.wrong_button)
		response_section_layout.addWidget(self.reopen_button)

		# Create the Player section
		player_section_layout = QtGui.QVBoxLayout(self)

		player1_section_layout = QtGui.QGridLayout(self)
		player1_name_label = QtGui.QLabel('Name')
		player1_points_label = QtGui.QLabel('Points')
		player1_name_text = QtGui.QLineEdit()
		player1_points_text = QtGui.QLineEdit()
		player1_points_text.setReadOnly(True)
		player1_widget = QtGui.QWidget(self)
		player1_widget.setPalette(QtGui.QPalette(QtGui.QColor(0,0,255)))
		player1_section_layout.addWidget(player1_name_label,0,0)
		player1_section_layout.addWidget(player1_name_text,0,1,1,2)
		player1_section_layout.addWidget(player1_points_label,1,0)
		player1_section_layout.addWidget(player1_points_text,1,1,1,2)

		player1_box = QtGui.QGroupBox('Player 1')
		player1_box.setLayout(player1_section_layout)
		player1_box.setAutoFillBackground(True)
		player1_box.setPalette(QtGui.QPalette(QtGui.QColor(0,0,255)))

		player_section_layout.addWidget(player1_box)

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

		# Create the KeyActions
		self.listen = False
		player_1_key_event = QtGui.QShortcut(QtGui.QKeySequence('1'),self)
		player_2_key_event = QtGui.QShortcut(QtGui.QKeySequence('2'),self)
		player_3_key_event = QtGui.QShortcut(QtGui.QKeySequence('3'),self)
		player_4_key_event = QtGui.QShortcut(QtGui.QKeySequence('4'),self)

		# Connecitong stuff to functions
		self.app.connect(quit,Qt.SIGNAL('pressed()'),lambda: self.quit())
		self.app.connect(self.correct_button,Qt.SIGNAL('pressed()'),lambda: self.correct())
		self.app.connect(self.wrong_button,Qt.SIGNAL('pressed()'),lambda: self.wrong())
		self.app.connect(self.reopen_button,Qt.SIGNAL('pressed()'),lambda: self.reopen())

		self.app.connect(player_1_key_event,Qt.SIGNAL('activated()'),lambda: self.player_pressed('p1'))
		self.app.connect(player_2_key_event,Qt.SIGNAL('activated()'),lambda: self.player_pressed('p2'))
		self.app.connect(player_3_key_event,Qt.SIGNAL('activated()'),lambda: self.player_pressed('p3'))
		self.app.connect(player_4_key_event,Qt.SIGNAL('activated()'),lambda: self.player_pressed('p4'))

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
