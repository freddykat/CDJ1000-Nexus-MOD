import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QFrame, QSlider, QMenuBar, QMenu, QAction, QListWidget, QListWidgetItem, QPushButton, QMenu, QSizePolicy, QColorDialog
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
import mido

class MidiThread(QThread):
    midi_message_received = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.midi_input = mido.open_input('Your MIDI Input Port Name', callback=self.handle_midi_input)
        self.midi_output = mido.open_output('Your MIDI Output Port Name')

    def run(self):
        self.exec_()

    def handle_midi_input(self, message):
        self.midi_message_received.emit(message)

    def send_midi_message(self, status, data1, data2):
        message = mido.Message(status, note=data1, velocity=data2)
        self.midi_output.send(message)

    def close_ports(self):
        self.midi_input.close()
        self.midi_output.close()

class ExtendedWaveformFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #777;")
        self.fixed_needle_position = 0.2  # Value between 0 and 1
        self.loop_markers = [(0.3, 0.4), (0.6, 0.7)]  # List of tuples (start, end) between 0 and 1
        self.slip_function_needle_position = 0.8  # Value between 0 and 1
        self._needle_color = Qt.red  # Default needle color
        self._marker_color = Qt.green  # Default marker color

        # Add Zoom Buttons
        self.zoom_in_button = QPushButton('+', self)
        self.zoom_in_button.clicked.connect(self.zoomIn)

        self.zoom_out_button = QPushButton('-', self)
        self.zoom_out_button.clicked.connect(self.zoomOut)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw Fixed Needle
        self.drawNeedle(painter, self.fixed_needle_position, self._needle_color)

        # Draw Loop Markers
        for start, end in self.loop_markers:
            self.drawNeedle(painter, start, self._marker_color)
            self.drawNeedle(painter, end, self._marker_color)

        # Draw Slip Function Needle
        self.drawNeedle(painter, self.slip_function_needle_position, Qt.blue)

    def drawNeedle(self, painter, position, color):
        rect = self.contentsRect()
        x = rect.x() + position * rect.width()
        y1 = rect.y()
        y2 = rect.y() + rect.height()

        painter.setPen(QColor(color))
        painter.setBrush(QColor(color))  # Fill the needle with the specified color
        painter.drawLine(x, y1, x, y2)

    def reset(self):
        self.update()

    def zoomIn(self):
        # Implement zoom in logic
        print("Zoom In")

    def zoomOut(self):
        # Implement zoom out logic
        print("Zoom Out")

    def setNeedleColor(self, color):
        self._needle_color = color
        self.update()

    def setMarkerColor(self, color):
        self._marker_color = color
        self.update()

    def needleColor(self):
        return self._needle_color

    def markerColor(self):
        return self._marker_color

class MyNexusApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        # Create and start the MIDI thread
        self.midi_thread = MidiThread(self)
        self.midi_thread.midi_message_received.connect(self.handle_midi_input)
        self.midi_thread.start()

    def initUI(self):
        self.top_bar = QLabel('Music Loaded', self)
        self.top_bar.setStyleSheet("background-color: #333; color: white; font-size: 16px; padding: 10px;")

        self.waveform_frame = ExtendedWaveformFrame(self)
        self.position_slider = QSlider(self)
        self.position_slider.setOrientation(Qt.Horizontal)
        self.position_slider.setStyleSheet("QSlider::handle:horizontal { background: #ccc; }")

        self.middle_waveform_frame = ExtendedWaveformFrame(self)

        self.artwork_label = QLabel(self)
        self.track_info_label = QLabel(self)
        self.updateCurrentTrack("Currently Playing Track", "Artist Name", "Album Name", "path/to/artwork.jpg")

        self.music_list_widget = QListWidget(self)
        self.populateMusicList()

        self.bar_counter_label = QLabel(self)
        self.bar_counter = 0
        self.bar_counter_label.setText(str(self.bar_counter))

        self.loop_button_touch = QPushButton('Loop', self)
        self.loop_button_touch.clicked.connect(self.showLoopMenu)
        self.loop_button_touch.setGeometry(10, 10, 100, 40)  # Adjust the position and size as needed

        self.beat_jump_button_touch = QPushButton('Beat Jump', self)
        self.beat_jump_button_touch.clicked.connect(self.showBeatJumpMenu)
        self.beat_jump_button_touch.setGeometry(120, 10, 100, 40)  # Adjust the position and size as needed

        self.loop_menu = QMenu(self)
        self.beat_jump_menu = QMenu(self)
        self.populateLoopMenu()
        self.populateBeatJumpMenu()

        self.loop_label = QLabel('Loop Division: -', self)
        self.loop_label.setGeometry(10, 70, 200, 30)  # Adjust the position and size as needed

        self.beat_jump_label = QLabel('Beat Jump: -', self)
        self.beat_jump_label.setGeometry(10, 110, 200, 30)  # Adjust the position and size as needed

        # Add Zoom Buttons
        self.zoom_in_button = QPushButton('+', self)
        self.zoom_in_button.clicked.connect(self.middle_waveform_frame.zoomIn)

        self.zoom_out_button = QPushButton('-', self)
        self.zoom_out_button.clicked.connect(self.middle_waveform_frame.zoomOut)

        layout = QVBoxLayout(self)
        layout.addWidget(self.top_bar)
        layout.addWidget(self.waveform_frame)
        layout.addWidget(self.position_slider)
        layout.addWidget(self.middle_waveform_frame)
        layout.addWidget(self.artwork_label)
        layout.addWidget(self.track_info_label)
        layout.addWidget(self.music_list_widget)
        layout.addWidget(self.bar_counter_label)
        layout.addWidget(self.loop_button_touch)
        layout.addWidget(self.beat_jump_button_touch)
        layout.addWidget(self.zoom_in_button)
        layout.addWidget(self.zoom_out_button)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateBarCounter)
        self.timer.start(500)  # Update every 500 milliseconds

        self.createMenus()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('My Nexus App')
        self.show()

    def handle_midi_input(self, message):
        # Handle MIDI input here
        print(f"MIDI Message Received: {message}")

    def createMenus(self):
        menubar = self.menuBar()

        # File Menu
        fileMenu = menubar.addMenu('File')

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        # Extended Configurations Sub-Menu
        extendedMenu = menubar.addMenu('Extended Configurations')

        # Music Source Sub-Menus
        musicSourcesMenu = menubar.addMenu('Music Sources')

        cdAction = QAction('CD', self)
        sdAction = QAction('SD', self)
        usbAction = QAction('USB', self)
        linkAction = QAction('LINK', self)

        cdAction.triggered.connect(self.handleMusicSourceSelected)
        sdAction.triggered.connect(self.handleMusicSourceSelected)
        usbAction.triggered.connect(self.handleMusicSourceSelected)
        linkAction.triggered.connect(self.handleMusicSourceSelected)

        musicSourcesMenu.addAction(cdAction)
        musicSourcesMenu.addAction(sdAction)
        musicSourcesMenu.addAction(usbAction)
        musicSourcesMenu.addAction(linkAction)

        # Add Color Customization Option
        colorAction = QAction('Customize Colors', self)
        colorAction.triggered.connect(self.customizeColors)
        extendedMenu.addAction(colorAction)

    def handleMusicSourceSelected(self):
        source = self.sender().text()
        self.top_bar.setText(f"Music Source Selected: {source}")

    def handleMouseMove(self, event):
        self.resetTimer()

    def resetTimer(self):
        self.timer.stop()
        self.timer.start(8000)

    def resetToMainMenu(self):
        self.top_bar.setText('Music Loaded')
        self.waveform_frame.reset()
        self.position_slider.setValue(0)
        self.middle_waveform_frame.reset()
        self.updateCurrentTrack("Currently Playing Track", "Artist Name", "Album Name", "path/to/artwork.jpg")

    def updateCurrentTrack(self, title, artist, album, artwork_path):
        self.track_info_label.setText(f"<b>{title}</b><br>{artist} - {album}")

        pixmap = QPixmap(artwork_path)
        self.artwork_label.setPixmap(pixmap.scaledToHeight(100))

    def populateMusicList(self):
        # Add some dummy items for demonstration
        for i in range(10):
            item = QListWidgetItem(f"Track {i}")
            self.music_list_widget.addItem(item)

    def longPressEvent(self):
        # Implement your extended functions here
        print("Long press event triggered!")

    def fastPressEvent(self):
        # Implement loading the track into the player here
        selected_item = self.music_list_widget.currentItem()
        if selected_item:
            print(f"Loading track: {selected_item.text()}")

    def updateBarCounter(self):
        # Update the bar counter based on the beats of the music
        # You should replace this logic with the actual beats detection or synchronization logic
        self.bar_counter += 1
        self.bar_counter_label.setText(str(self.bar_counter))

    def showLoopMenu(self):
        loop_button_rect = self.loop_button_touch.rect()
        loop_button_pos = self.loop_button_touch.mapToGlobal(loop_button_rect.bottomLeft())
        self.loop_menu.exec_(loop_button_pos)

    def showBeatJumpMenu(self):
        beat_jump_button_rect = self.beat_jump_button_touch.rect()
        beat_jump_button_pos = self.beat_jump_button_touch.mapToGlobal(beat_jump_button_rect.bottomLeft())
        self.beat_jump_menu.exec_(beat_jump_button_pos)

    def populateLoopMenu(self):
        loop_divisions = ['16 bars', '8 bars', '4 bars', '2 bars', '1 bar', '1/2 bar', '1/4 bar', '1/8 bar']

        # Loop Sub-Menu
        loop_submenu = self.loop_menu.addMenu('Loop Subdivisions')
        for division in loop_divisions:
            action = loop_submenu.addAction(division)
            action.triggered.connect(self.handleLoopDivisionSelected)

    def populateBeatJumpMenu(self):
        beat_jump_values = ['16 bars', '8 bars', '4 bars', '2 bars', '1 bar', '1/2 bar', '1/4 bar', '1/8 bar']

        # Beat Jump Sub-Menu
        beat_jump_submenu = self.beat_jump_menu.addMenu('Beat Jump')
        for value in beat_jump_values:
            action = beat_jump_submenu.addAction(value)
            action.triggered.connect(self.handleBeatJumpSelected)

    def handleLoopDivisionSelected(self):
        division = self.sender().text()
        self.loop_label.setText(f'Loop Division: {division}')

    def handleBeatJumpSelected(self):
        value = self.sender().text()
        self.beat_jump_label.setText(f'Beat Jump: {value}')

    def customizeColors(self):
        # Create a dialog to customize colors
        dialog = QColorDialog(self)
        dialog.setWindowTitle('Customize Colors')

        # Get the colors for needles and markers
        needle_color = dialog.getColor(self.middle_waveform_frame.needleColor(), self, 'Choose Needle Color')
        marker_color = dialog.getColor(self.middle_waveform_frame.markerColor(), self, 'Choose Marker Color')

        # Update the colors
        self.middle_waveform_frame.setNeedleColor(needle_color)
        self.middle_waveform_frame.setMarkerColor(marker_color)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    nexus_app = MyNexusApp()
    sys.exit(app.exec_())
