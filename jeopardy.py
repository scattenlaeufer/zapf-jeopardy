#!/usr/bin/python

import sys, os, json, subprocess, random, serial
import argparse
from textwrap import wrap
from PyQt4 import QtGui, QtCore, Qt, phonon
from time import sleep

#TODO:
#    Speichern
#    Mediacontrolsteuerung setting

name = 'ZaPF-Jeopardy (v0.1)'
points_factor = 100

serial_path = '/dev/ttyUSB0'

font_size_wall = 25
font_size_answer = 40
font_size_player = 25

color_1 = [255, 165, 100]
color_2 = [255, 255, 0]
color_3 = [0, 255, 0]
color_4 = [0, 255, 255]

backup_name = 'game_backup'

if os.path.exists(serial_path):
    use_button_box = True
else:
    use_button_box = False

class Jeopardy_Wall(QtGui.QWidget):

    def __init__(self,file_head):
        super(Jeopardy_Wall,self).__init__()
        self.grid = QtGui.QGridLayout(self)

        self.file_head = file_head

        jeopardy_wall_layout = QtGui.QHBoxLayout(None)

        self.wall_button = []
        self.wall_category_boxes = []
        self.wall_category_layouts = []

        for i in range(5):
            self.wall_button.append([])
            self.wall_category_layouts.append(QtGui.QVBoxLayout(None))
            self.wall_category_boxes.append(QtGui.QGroupBox(''))
            self.wall_category_boxes[i].setLayout(self.wall_category_layouts[i])
            jeopardy_wall_layout.addWidget(self.wall_category_boxes[i])
            for j in range(5):
                self.wall_button[i].append(QtGui.QPushButton(str((j+1)*points_factor)))
                self.wall_button[i][j].setSizePolicy(QtGui.QSizePolicy.Ignored,QtGui.QSizePolicy.Ignored)
                self.wall_category_layouts[i].addWidget(self.wall_button[i][j])

        self.player_wall_layout = QtGui.QHBoxLayout(None)

        self.jeopardy_wall_box = QtGui.QGroupBox('Jeopardy board')
        wall_font = self.jeopardy_wall_box.font()
        wall_font.setPointSize(font_size_wall)
        self.jeopardy_wall_box.setFont(wall_font)
        self.jeopardy_wall_box.setLayout(jeopardy_wall_layout)


        player_wall_box = QtGui.QGroupBox('Player')
        player_wall_box.setLayout(self.player_wall_layout)

        answer_layout = QtGui.QVBoxLayout(None)
        self.answer_label = QtGui.QLabel('')
        self.answer_label.setHidden(True)
        answer_font = self.font()
        answer_font.setPointSize(font_size_answer)
        self.answer_label.setFont(answer_font)
        self.video_player = phonon.Phonon.VideoPlayer(phonon.Phonon.VideoCategory,None)
        self.video_player.setHidden(True)
        answer_layout.addWidget(self.answer_label)
        answer_layout.addWidget(self.video_player)
        self.answer_box = QtGui.QGroupBox('Answer')
        self.answer_box.setLayout(answer_layout)
        self.answer_box.setHidden(True)

        self.grid.addWidget(self.answer_box,0,0,8,0)
        self.grid.addWidget(self.jeopardy_wall_box,0,0,8,0)
        self.grid.addWidget(player_wall_box,9,0)

    def resizeEvent(self,r):
            self.answer_label.setAlignment(QtCore.Qt.AlignCenter)

    def set_categories(self,categories):
        for i in range(len(categories)):
            self.wall_category_boxes[i].setTitle(categories[i])

    def scale(self,media):
        media_size = media.size()
        label_size = self.answer_label.size()
        media_ratio = float(media_size.width()) / float(media_size.height())
        label_ratio = float(label_size.width()) / float(label_size.height())
        scale_factor = 0.5
        if media_size.width() > label_size.width() or media_size.height() > label_size.height():
            if media_ratio < label_ratio:
                return media.scaledToHeight(label_size.height())
            else:
                return media.scaledToWidth(label_size.width())
        elif media_ratio > label_ratio and float(media_size.width()) / float(label_size.width()) < scale_factor:
            return media.scaledToWidth(int(label_size.width() * scale_factor))
        elif float(media_size.height()) / float(label_size.height()) < scale_factor:
            return media.scaledToHeight(int(label_size.height() * scale_factor))
        return media

    def present_answer(self,type,answer):
        self.jeopardy_wall_box.setHidden(True)
        self.answer_box.setHidden(False)
        if type == 'text':
            self.answer_label.setHidden(False)
            self.answer_label.setText('\n'.join(wrap(answer,50)))
        elif type == 'image':
            self.answer_label.setHidden(False)
            image = self.scale(QtGui.QPixmap(os.path.join(self.file_head,answer)))
            self.answer_label.setPixmap(image)
        elif type == 'video':
            self.video_player.setHidden(False)
            media_source = phonon.Phonon.MediaSource(os.path.join(self.file_head,answer))
            self.video_player.play(media_source)
            # self.video_player.play()
            # print(media_source)
            # print(self.video_player.mediaObject())
            # print(os.path.join(self.file_head,answer))
            # print(self.video_player.isPlaying())
            # print(self.video_player.isPaused())
            # print(self.video_player.totalTime())
        elif type == 'audio':
            self.answer_label.setHidden(False)
            self.answer_label.setText('listen up!')
            self.audio = Jeopardy.Music(os.path.join(self.file_head,answer))
            self.audio.play()

    def clear_answer_section(self,type):
        self.answer_label.setHidden(True)
        self.video_player.setHidden(True)
        self.answer_box.setHidden(True)
        self.jeopardy_wall_box.setHidden(False)


class Jeopardy(QtGui.QWidget):

    # Class for the individual players
    class Player:

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
            self.detect_button = QtGui.QPushButton('detect')
            if not use_button_box:
                self.detect_button.setEnabled(False)

            layout.addWidget(name_label,0,0)
            layout.addWidget(self.name_text,0,1,1,2)
            layout.addWidget(points_label,1,0)
            layout.addWidget(self.points_text,1,1,1,2)
            layout.addWidget(rename_button,2,0)
            layout.addWidget(bonus_button,2,1)
            layout.addWidget(self.detect_button, 2, 2)

            self.box = QtGui.QGroupBox(name)
            self.box.setLayout(layout)
            self.box.setAutoFillBackground(True)
            self.box.setPalette(self.color)

            wall_layout = QtGui.QHBoxLayout(None)
            wall_points_label = QtGui.QLabel('points')
            self.wall_points_text = QtGui.QLineEdit()
            self.wall_points_text.setReadOnly(True)
            self.wall_points_text.setText(str(self.points))
            wall_layout.addWidget(wall_points_label)
            wall_layout.addWidget(self.wall_points_text)

            self.wall_box = QtGui.QGroupBox(name)
            wall_box_font = self.wall_box.font()
            wall_box_font.setPointSize(font_size_player)
            self.wall_box.setFont(wall_box_font)
            self.wall_box.setLayout(wall_layout)
            self.wall_box.setAutoFillBackground(True)
            self.wall_box.setPalette(self.color)

            self.app.connect(rename_button,Qt.SIGNAL('pressed()'),lambda: self.rename())
            self.app.connect(bonus_button,Qt.SIGNAL('pressed()'),lambda: self.bonus())

        def rename(self):
            text, ok = QtGui.QInputDialog.getText(None,'rename '+self.name, 'enter new name:')
            if ok and text != '':
                self.name = text
                self.name_text.setText(self.name)
                self.wall_box.setTitle(self.name)

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
            self.wall_points_text.setText(str(self.points))

    class Music(QtCore.QObject):

        def __init__(self,source="data/music.ogg"):
            super(Jeopardy.Music,self).__init__()
            output = phonon.Phonon.AudioOutput(phonon.Phonon.MusicCategory,self)
            self.media = phonon.Phonon.MediaObject(self)
            phonon.Phonon.createPath(self.media, output)
            self.media.setCurrentSource(phonon.Phonon.MediaSource(source))

        def play(self):
            if self.media.state() != phonon.Phonon.PlayingState:
                self.media.play()

        def pause(self):
            if self.media.state() == phonon.Phonon.PlayingState:
                self.media.pause()

        def stop(self):
            if self.media.state() == phonon.Phonon.PlayingState or self.media.state() == phonon.Phonon.PausedState:
                self.media.stop()

    class SerialCommunicator(QtCore.QThread):

        buttonpress = QtCore.pyqtSignal(int)

        def __init__(self, app, serialport=serial_path, baudrate=9600):
            super(Jeopardy.SerialCommunicator, self).__init__()
            self.app = app

            self.read_interval = 200

            self.ser = serial.Serial(serialport, baudrate, timeout=self.read_interval/1000)

            self.timer = QtCore.QTimer()
            self.timer.moveToThread(self)
            self.timer.setInterval(self.read_interval)
            self.app.connect(self.timer, Qt.SIGNAL('timeout()'), self.stuff)

        def run(self):
            self.ser.reset_input_buffer()
            self.timer.start()
            self.exec_()

        def stuff(self):
            ser_output = None
            ser_output = self.ser.read()
            if ser_output:
                self.buttonpress.emit(int(ser_output.decode()))

    def __init__(self, app, game_file, load=False):
        super(Jeopardy,self).__init__()
        print(name)
        self.app = app
        self.double_jeopardy = False
        self.active_player = None
        self.music = self.Music()
        if use_button_box:
            self.serialCom = self.SerialCommunicator(app)

        self.button_list = ['p1', 'p2', 'p3', 'p4']
        self.detect_functions = {}

        game_str = ''
        with open(game_file,'r') as file:
            game_str = file.read()
        if load:
            self.game_backup = json.loads(game_str)
            self.game_data = self.game_backup['game_data']
        else:
            self.game_data = json.loads(game_str)
        game_dir_head = os.path.split(game_file)[0]

        jeopardy_categories = []
        for i in self.game_data:
            jeopardy_categories.append(i['category'])

        self.grid = QtGui.QGridLayout(self)

        # Create the Jeopardy window
        jeopardy_window = QtGui.QHBoxLayout(None)
        jeopardy_board_box = QtGui.QGroupBox('Jeopardy board')
        jeopardy_board_box.setLayout(jeopardy_window)
        jeopardy_category_layouts = []
        self.jeopardy_category_boxes = []

        # Create the Jeopardy buttons
        self.jeopardy_button = []
        for i in range(5):
            jeopardy_category_layouts.append(QtGui.QVBoxLayout(None))
            self.jeopardy_category_boxes.append(QtGui.QGroupBox(jeopardy_categories[i]))
            self.jeopardy_button.append([])
            for j in range(5):
                self.jeopardy_button[i].append(QtGui.QPushButton(str((j+1)*points_factor)))
                self.jeopardy_button[i][j].setSizePolicy(QtGui.QSizePolicy.Ignored,QtGui.QSizePolicy.Ignored)
                jeopardy_category_layouts[i].addWidget(self.jeopardy_button[i][j])
                self.app.connect(self.jeopardy_button[i][j],Qt.SIGNAL('pressed()'),lambda i=[i,j]: self.select_field(i[0],i[1]))
            self.jeopardy_category_boxes[i].setLayout(jeopardy_category_layouts[i])
            jeopardy_window.addWidget(self.jeopardy_category_boxes[i])

        # Create the Answer section
        self.answer_label = QtGui.QLabel('')
        self.answer_label.setAlignment(QtCore.Qt.AlignCenter)
        self.answer_play_button = QtGui.QPushButton('play')
        self.answer_pause_button = QtGui.QPushButton('pause')
        self.answer_stop_button = QtGui.QPushButton('stop')
        self.answer_play_button.setHidden(True)
        self.answer_pause_button.setHidden(True)
        self.answer_stop_button.setHidden(True)
        answer_layout = QtGui.QHBoxLayout(None)
        answer_layout.addWidget(self.answer_label)
        answer_layout.addWidget(self.answer_play_button)
        answer_layout.addWidget(self.answer_pause_button)
        answer_layout.addWidget(self.answer_stop_button)
        answer_box = QtGui.QGroupBox('presented answer')
        answer_box.setLayout(answer_layout)

        self.question_label = QtGui.QLabel('')
        self.question_label.setAlignment(QtCore.Qt.AlignCenter)
        question_layout = QtGui.QHBoxLayout(None)
        question_layout.addWidget(self.question_label)
        question_box = QtGui.QGroupBox('suggested question')
        question_box.setLayout(question_layout)

        answer_section_layout = QtGui.QVBoxLayout(None)
        answer_section_layout.addWidget(answer_box)
        answer_section_layout.addWidget(question_box)

        # Create the Repsonse section
        response_section_layout = QtGui.QVBoxLayout(None)
        self.correct_button = QtGui.QPushButton('CORRECT')
        self.correct_button.setPalette(QtGui.QPalette(QtGui.QColor(0,255,0)))
        self.wrong_button = QtGui.QPushButton('WRONG')
        self.wrong_button.setPalette(QtGui.QPalette(QtGui.QColor(255,0,0)))
        self.reopen_button = QtGui.QPushButton('REOPEN')
        self.set_response(False)
        self.reopen_button.setEnabled(False)

        response_section_layout.addWidget(self.correct_button)
        response_section_layout.addWidget(self.wrong_button)
        response_section_layout.addWidget(self.reopen_button)

        # Create the Player section
        player_section_layout = QtGui.QVBoxLayout(None)
        player_box = QtGui.QGroupBox('Player')
        player_box.setLayout(player_section_layout)

        self.player = {}
        self.player['p1'] = self.Player(self.app,'Player 1', color_1)
        self.player['p2'] = self.Player(self.app,'Player 2', color_2)
        self.player['p3'] = self.Player(self.app,'Player 3', color_3)
        self.player['p4'] = self.Player(self.app,'Player 4', color_4)

        player_section_layout.addWidget(self.player['p1'].box)
        player_section_layout.addWidget(self.player['p2'].box)
        player_section_layout.addWidget(self.player['p3'].box)
        player_section_layout.addWidget(self.player['p4'].box)

        # Create the Global Butten section
        global_button_layout = QtGui.QVBoxLayout(None)

        quit = QtGui.QPushButton('quit')
        self.random_player_button = QtGui.QPushButton('random player')
        self.music_checkbox = QtGui.QCheckBox('play Jeoprady music')
        self.music_checkbox.setCheckState(0)
        global_button_layout.addWidget(self.music_checkbox)
        global_button_layout.addWidget(self.random_player_button)
        global_button_layout.addWidget(quit)

        # Add everything to the grid
        self.grid.addWidget(jeopardy_board_box,0,0,4,4)
        self.grid.addLayout(answer_section_layout,5,1,1,3)
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
        self.app.connect(self.random_player_button,Qt.SIGNAL('pressed()'),lambda: self.randomize_player())
        self.app.connect(self.correct_button,Qt.SIGNAL('pressed()'),lambda: self.correct())
        self.app.connect(self.wrong_button,Qt.SIGNAL('pressed()'),lambda: self.wrong())
        self.app.connect(self.reopen_button,Qt.SIGNAL('pressed()'),lambda: self.reopen())

        self.app.connect(self.answer_play_button,Qt.SIGNAL('pressed()'),lambda: self.answer_play())
        self.app.connect(self.answer_pause_button,Qt.SIGNAL('pressed()'),lambda: self.answer_pause())
        self.app.connect(self.answer_stop_button,Qt.SIGNAL('pressed()'),lambda: self.answer_stop())

        self.randomize_player()

        self.app.connect(player_1_key_event,Qt.SIGNAL('activated()'),lambda: self.player_pressed('p1'))
        self.app.connect(player_2_key_event,Qt.SIGNAL('activated()'),lambda: self.player_pressed('p2'))
        self.app.connect(player_3_key_event,Qt.SIGNAL('activated()'),lambda: self.player_pressed('p3'))
        self.app.connect(player_4_key_event,Qt.SIGNAL('activated()'),lambda: self.player_pressed('p4'))

        self.app.connect(self.player['p1'].detect_button, Qt.SIGNAL('pressed()'), lambda: self.detect_button('p1'))
        self.app.connect(self.player['p2'].detect_button, Qt.SIGNAL('pressed()'), lambda: self.detect_button('p2'))
        self.app.connect(self.player['p3'].detect_button, Qt.SIGNAL('pressed()'), lambda: self.detect_button('p3'))
        self.app.connect(self.player['p4'].detect_button, Qt.SIGNAL('pressed()'), lambda: self.detect_button('p4'))

        if use_button_box:
            self.serialCom.buttonpress.connect(self.serial_input)

        self.setLayout(self.grid)
        self.setWindowTitle(name)

        self.wall = Jeopardy_Wall(game_dir_head)
        self.wall.set_categories(jeopardy_categories)

        if load:
            for index, player in self.game_backup['player'].items():
                self.player[index].name = player['name']
                self.player[index].name_text.setText(player['name'])
                self.player[index].wall_box.setTitle(player['name'])
                self.player[index].add_points(player['points'])
            for i in range(5):
                for j in range(5):
                    self.wall.wall_button[i][j].setText(self.game_backup['wall'][i][j]['text'])
                    self.jeopardy_button[i][j].setText(self.game_backup['wall'][i][j]['text'])
                    button_color = QtGui.QPalette(QtGui.QColor(
                                                               self.game_backup['wall'][i][j]['color'][0],
                                                               self.game_backup['wall'][i][j]['color'][1],
                                                               self.game_backup['wall'][i][j]['color'][2]
                                                               ))
                    self.wall.wall_button[i][j].setPalette(button_color)
                    self.jeopardy_button[i][j].setPalette(button_color)
        else:
            self.game_backup = {}
            self.game_backup['game_data'] = self.game_data
            self.save()

        self.wall.player_wall_layout.addWidget(self.player['p1'].wall_box)
        self.wall.player_wall_layout.addWidget(self.player['p2'].wall_box)
        self.wall.player_wall_layout.addWidget(self.player['p3'].wall_box)
        self.wall.player_wall_layout.addWidget(self.player['p4'].wall_box)

        self.show()
#        self.showMaximized()
        self.wall.show()

    def detect_button(self, player):
        if use_button_box:
            self.detect_functions[player] = lambda x: self.return_serial_input(player, x)
            self.serialCom.buttonpress.connect(self.detect_functions[player])
            self.serialCom.start()

    def return_serial_input(self, player, output):
        if use_button_box:
            self.serialCom.exit()
            self.serialCom.buttonpress.disconnect(self.detect_functions[player])
            self.button_list[output] = player
            self.player[player].detect_button.setText(str(output))

    def serial_input(self, output):
        if use_button_box:
            self.serialCom.exit()
            if self.listen:
                self.player_pressed(self.button_list[output])

    def save(self):
        self.game_backup['player'] = {}
        for index, player in self.player.items():
            player_backup = {}
            player_backup['name'] = player.name
            player_backup['points'] = player.points
            self.game_backup['player'][index] = player_backup
        self.game_backup['wall'] = []
        for button_row in self.wall.wall_button:
            row_list = []
            for button in button_row:
                button_dict = {}
                button_dict['text'] = button.text()
                button_color = button.palette().color(1)
                button_dict['color'] = [button_color.red(), button_color.green(), button_color.blue()]
                row_list.append(button_dict)
            self.game_backup['wall'].append(row_list)
        json_backup = json.dumps(self.game_backup, sort_keys=True, indent=4)
        with open(backup_name, 'w') as backup_file:
            backup_file.write(json_backup)

    def quit(self):
        if use_button_box:
            self.serialCom.exit()
        message = QtGui.QMessageBox(4,'quit Jeoarpardy?','you really think, you might\nbe allowed to quit Jeopardy?',QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        resp = message.exec_()
        if resp == 16384:
            self.app.quit()
        elif use_button_box:
            self.serialCom.start()

    def randomize_player(self):
        self.active_player = 'p' + str(random.randint(1,4))
        self.random_player_button.setPalette(self.player[self.active_player].color)

    def wrap(self,text):
        return '\n'.join(wrap(text,110))

    def select_field(self,category_id,level):
        if self.active_player != None:
            if self.game_data[category_id]['level'][level]['double_jeopardy']:
                self.double_jeopardy = True
                ok = False
                self.wall.jeopardy_wall_box.setHidden(True)
                self.wall.answer_box.setHidden(False)
                self.wall.answer_label.setHidden(False)
                image = self.wall.scale(QtGui.QPixmap(os.path.abspath(os.path.join('data','double_jeopardy.png'))))
                # print(image)
                self.wall.answer_label.setPixmap(image)
                while not ok:
                    self.points_set,ok = QtGui.QInputDialog().getInt(None,'DOUBLE JEOPARDY','double jeopardy\nbet '+str((level+1)*points_factor)+' to '+str((level+1)*2*points_factor)+' points',(level+1)*points_factor,(1+level)*points_factor,(1+level)*points_factor*2)
                self.wall.answer_label.setHidden(True)

            self.current_field = [category_id,level]
            self.jeopardy_button[category_id][level].setPalette(QtGui.QPalette(QtGui.QColor(255,255,255)))
            self.type_video = self.game_data[category_id]['level'][level]['type'] in ['video']
            self.type_audio = self.game_data[category_id]['level'][level]['type'] in ['audio']
            if self.double_jeopardy:
                self.player_pressed(self.active_player)
            else:
                self.listen = True
                if use_button_box:
                    self.serialCom.start()
                self.set_field_activity(False)
                if self.music_checkbox.checkState() == 2 and not (self.type_video or self.type_audio):
                    self.music.play()
            if self.type_video or self.type_audio:
                self.answer_label.setHidden(True)
                self.answer_play_button.setHidden(False)
                self.answer_pause_button.setHidden(False)
                self.answer_stop_button.setHidden(False)
            self.reopen_button.setEnabled(True)
            self.wall.present_answer(self.game_data[category_id]['level'][level]['type'],self.game_data[category_id]['level'][level]['answer'])
            if self.game_data[category_id]['level'][level]['type'] == 'text':
                self.answer_label.setText(self.wrap(self.game_data[category_id]['level'][level]['answer'],))
            elif self.game_data[category_id]['level'][level]['type'] == 'image':
                self.answer_label.setText('image')
            self.question_label.setText(self.wrap(self.game_data[category_id]['level'][level]['question']))
        else:
            message = QtGui.QMessageBox(3,'select player','a player must be selected.\nchoose one at random')
            message.exec_()

    def player_pressed(self,player_id):
        if use_button_box:
            if self.serialCom.isRunning():
                self.serialCom.exit()
        if self.listen:
            self.music.stop()
        if self.listen or self.double_jeopardy:
            if self.type_video:
                self.wall.video_player.pause()
            elif self.type_audio:
                self.wall.audio.pause()
            self.listen = False
            self.set_response(True)
            self.active_player = player_id
            for i in self.player:
                if i != player_id:
                    self.player[i].wall_box.setPalette(self.palette())
                    self.player[i].box.setPalette(self.palette())

    def reset_player_color(self):
        for i in self.player:
            self.player[i].wall_box.setPalette(self.player[i].color)
            self.player[i].box.setPalette(self.player[i].color)

    def clear_answer_section(self):
        self.reset_player_color()
        #if self.game_data[self.current_field[0]]['level'][self.current_field[1]]['type'] == 'text':
        if self.type_video or self.type_audio:
            self.answer_play_button.setHidden(True)
            self.answer_pause_button.setHidden(True)
            self.answer_stop_button.setHidden(True)
            self.answer_label.setHidden(False)
        self.answer_label.setText('')
        self.question_label.setText('')
        self.wall.clear_answer_section(self.game_data[self.current_field[0]]['level'][self.current_field[1]]['type'])

    def correct(self):
        self.set_response(False)
        self.set_field_activity(True)
        self.reopen_button.setEnabled(False)
        button = self.jeopardy_button[self.current_field[0]][self.current_field[1]]
        wall_button = self.wall.wall_button[self.current_field[0]][self.current_field[1]]
        player = self.player[self.active_player]
        if self.listen or self.double_jeopardy:
            if self.type_video:
                self.wall.video_player.pause()
            elif self.type_audio:
                self.wall.audio.pause()
        if self.double_jeopardy:
            title = str(button.text())+'\n'+player.name+' [✓] [DJ]'
            player.add_points(self.points_set)
            self.double_jeopardy = False
        else:
            title = str(button.text())+'\n'+player.name+' [✓]'
            player.add_points((self.current_field[1]+1)*points_factor)
        button.setPalette(player.color)
        button.setText(title)
        wall_button.setPalette(player.color)
        wall_button.setText(title)
        self.clear_answer_section()
        self.save()

    def wrong(self,points_set=0):
        self.set_response(False)
        self.set_field_activity(False)
        self.listen = True
        if use_button_box:
            self.serialCom.start()
        player = self.player[self.active_player]
        button = self.jeopardy_button[self.current_field[0]][self.current_field[1]]
        if self.double_jeopardy:
            title = str(button.text())+'\n'+player.name+' [✗] [DJ]'
            player.add_points(self.points_set*-1)
            self.double_jeopardy = False
        else:
            title = str(button.text())+'\n'+player.name+' [✗]'
            player.add_points((self.current_field[1]+1)*points_factor*-1)
        button.setText(title)
        self.wall.wall_button[self.current_field[0]][self.current_field[1]].setText(title)
        self.reset_player_color()
        if self.music_checkbox.checkState() == 2 and not (self.type_video or self.type_audio):
            self.music.play()
        if self.type_video:
            self.wall.video_player.play()
        elif self.type_audio:
            self.wall.audio.play()
        self.save()

    def reopen(self):
        if self.listen:
            self.set_response(False)
            self.set_field_activity(True)
            self.reopen_button.setEnabled(False)
            self.clear_answer_section()
            self.music.stop()
            if self.type_video:
                self.wall.video_player.pause()
            elif self.type_audio:
                self.wall.audio.pause()
            if use_button_box:
                self.serialCom.exit()
        else:
            self.reset_player_color()
            self.listen = True
            if use_button_box:
                self.serialCom.start()
            self.set_response(False)
            if self.type_video:
                self.wall.video_player.play()
            elif self.type_audio:
                self.wall.audio.play()
            if self.music_checkbox.checkState() == 2 and not (self.type_video or self.audio):
                self.music.play()
            if self.double_jeopardy:
                self.double_jeopardy = False

    def answer_play(self):
        if self.type_video:
            self.wall.video_player.play()
        elif self.type_audio:
            self.wall.audio.play()

    def answer_pause(self):
        if self.type_video:
            self.wall.video_player.pause()
        elif self.type_audio:
            self.wall.audio.pause()

    def answer_stop(self):
        if self.type_video:
            self.wall.video_player.stop()
        elif self.type_audio:
            self.wall.audio.stop()

    def set_response(self,a):
        self.correct_button.setEnabled(a)
        self.wrong_button.setEnabled(a)

    def set_field_activity(self,a):
        for i in self.jeopardy_button:
            for j in i:
                j.setEnabled(a)


def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Jeopardy')

    parser = argparse.ArgumentParser(description='a jeopardy')
    parser.add_argument('--load', default=False, action='store_true', help='load a saved game')
    parser.add_argument('game_file', metavar='GAME_FILE', type=str, nargs=1, help='a game to play')
    args = parser.parse_args()

    jeopardy = Jeopardy(app, args.game_file[0], args.load)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
