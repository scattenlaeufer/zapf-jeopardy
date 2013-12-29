#!/usr/bin/python

import sys
from PyQt4 import QtGui, QtCore, Qt

name = 'ZaPF-Jeopardy (v0.1)'

class Jeopardy(QtGui.QWidget):

	class Player:

		def rename(self):
			text, ok = QtGui.QInputDialog.getText(None,'rename '+self.name, 'enter new name:')
			if ok and text != '':
				self.name = text
				self.name_text.setText(self.name)


		def bonus(self):
			bonus_points, ok = QtGui.QInputDialog.getText(None,'bouns points','give '+self.name+' bonus points:')
			if ok and bonus_points != '':
				try:
					self.add_points(int(bonus_points))
				except ValueError:
					message = QtGui.QMessageBox(3,'ValueError','points must be integer!\nnoting will happen')
					message.exec_()

		def add_points(self,points):
			self.points += points
			self.points_text.setText(str(self.points))

		def __init__(self,app,name,color,points=0):
			self.app = app
			self.name = name
			self.points = points
			self.color = QtGui.QPalette(QtGui.QColor(color[0],color[1],color[2]))

			layout = QtGui.QGridLayout(None)
			name_label = QtGui.QLabel('Name')
			points_label = QtGui.QLabel('Points')
			self.name_text = QtGui.QLineEdit()
			self.name_text.setText(self.name)
			self.name_text.setReadOnly(True)
			self.points_text = QtGui.QLineEdit()
			self.points_text.setReadOnly(True)
			self.points_text.setText(str(self.points))
			rename_button = QtGui.QPushButton('rename')
			bonus_button = QtGui.QPushButton('bonus')
			
			layout.addWidget(name_label,0,0)
			layout.addWidget(self.name_text,0,1,1,2)
			layout.addWidget(points_label,1,0)
			layout.addWidget(self.points_text,1,1,1,2)
			layout.addWidget(rename_button,2,0)
			layout.addWidget(bonus_button,2,1)
	
			self.box = QtGui.QGroupBox(name)
			self.box.setLayout(layout)
			self.box.setAutoFillBackground(True)
			self.box.setPalette(self.color)

			self.app.connect(rename_button,Qt.SIGNAL('pressed()'),lambda: self.rename())
			self.app.connect(bonus_button,Qt.SIGNAL('pressed()'),lambda: self.bonus())


	def quit(self):
		message = message = QtGui.QMessageBox(4,'quit Jeoarpardy?','you really think, you might\nbe allowed to quit Jeopardy?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		resp = message.exec_()
		if resp == 16384:
			self.app.quit()


	def select_field(self,category_id,level):
		self.current_field = [category_id,level]
		self.jeopardy_button[category_id][level].setPalette(QtGui.QPalette(QtGui.QColor(255,255,255)))
		self.listen = True
		self.set_field_activity(False)


	def correct(self):
		self.set_response(False)
		self.set_field_activity(True)
		button = self.jeopardy_button[self.current_field[0]][self.current_field[1]]
		player = self.player[self.active_player]
		button.setPalette(player.color)
		button.setText(str(button.text())+'\n'+player.name+'[✓]')
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
			self.listen = False
			self.set_response(True)
			self.active_player = player_id


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
		jeopardy_window = QtGui.QHBoxLayout(None)
		jeopardy_category_layouts = []
		jeopardy_categories = ['test1','test2','test3','test4','test5']
		self.jeopardy_category_label = []

		# Create the Jeopardy buttons
		self.jeopardy_button = []
		for i in range(5):
			jeopardy_category_layouts.append(QtGui.QVBoxLayout(None))
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
		answer_section_layout = QtGui.QHBoxLayout(None)

		answer_box = QtGui.QGroupBox('Answer')
		answer_box.setLayout(answer_section_layout)

		# Create the Repsonse section
		response_section_layout = QtGui.QVBoxLayout(None)
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
		player_section_layout = QtGui.QVBoxLayout(None)
		player_box = QtGui.QGroupBox('Player')
		player_box.setLayout(player_section_layout)

		self.player = {}
		self.player['p1'] = self.Player(self.app,'Player 1',[0,0,255])
		self.player['p2'] = self.Player(self.app,'Player 2',[255,0,0])
		self.player['p3'] = self.Player(self.app,'Player 3',[0,255,0])
		self.player['p4'] = self.Player(self.app,'Player 4',[255,255,0])

		player_section_layout.addWidget(self.player['p1'].box)
		player_section_layout.addWidget(self.player['p2'].box)
		player_section_layout.addWidget(self.player['p3'].box)
		player_section_layout.addWidget(self.player['p4'].box)

		# Create the Global Butten section
		global_button_layout = QtGui.QVBoxLayout(None)

		quit = QtGui.QPushButton('quit')
		global_button_layout.addWidget(quit)

		# Add everything to the grid
		self.grid.addLayout(jeopardy_window,0,0,4,4)
		self.grid.addWidget(answer_box,5,1,1,3)
		self.grid.addWidget(player_box,0,5,4,1)
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
