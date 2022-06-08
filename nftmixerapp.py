import sys, os, json
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from mixer import Mixer
from exceptions import ComponentsPathError, LayersOrderFileError, ExceptionsFileError, RarityFileError

class Lexend(QtGui.QFont):
    def __init__(self, font_size, bold=False):
        super().__init__()
        self.add_font()
        self.setBold(bold)
        self.setPointSize(font_size)

    def add_font(self):
        font_path = os.getcwd() + '/fonts/Lexend.ttf'
        if not 'Lexend' in QtGui.QFontDatabase().families():
            if os.path.isfile(font_path):
                QtGui.QFontDatabase().addApplicationFont(font_path)
                self.setFamily('Lexend')
            else:
                self.setFamily('Arial')
        else:
            self.setFamily('Lexend')

class QLineEditExtended(QtWidgets.QLineEdit):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.clicked.emit()

class QLineEditDigitsOnly(QtWidgets.QLineEdit):
    def __init__(self):
        super().__init__()
        self.textChanged.connect(self.textChangedEvent)

    def textChangedEvent(self):
        digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        text = list(self.text())
        for i in range(len(text)):
            if not text[i] in digits:
                text[i] = ''
        self.setText(''.join(text))

class QWidgetExtended(QtWidgets.QWidget):
    resized = pyqtSignal()
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resized.emit()


class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mixer = Mixer()
        self.define_variables()
        self.window_settings()
        self.initial_settings()

    def define_variables(self):
        self.title_font_size = 18
        self.status_font_size = 12
        self.info_font_size = 14
        self.error_color = '#c91414'
        self.warning_color = '#fa0'
        self.correct_color = '#62ff00'
        self.hint_color = '#bbb'
        self.path_input_valid = False
        self.layers_order_input_valid = False
        self.file_input_valid = True
        self.rarity_input_valid = True

    def window_settings(self):
        self.setWindowTitle('NFTs Mixer')
        self.screen_width = QApplication.primaryScreen().size().width()
        self.screen_height = QApplication.primaryScreen().size().height()
        self.current_width = self.width
        self.current_height = self.height
        self.width = int(0.5 * self.screen_width)
        self.height = int(0.7 * self.screen_height)
        self.setGeometry(int((self.screen_width - self.width) / 2), int((self.screen_height - self.height) / 2), self.width, self.height)
        self.setStyleSheet('background-color: #888;')

    def initial_settings(self):
        self.path_layout = QtWidgets.QVBoxLayout()
        self.path_layout_widget = QtWidgets.QWidget()
        self.path_layout_widget.setLayout(self.path_layout)
        self.path_layout.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.path_layout_widget)

        path_label = QtWidgets.QLabel()
        path_label.setText('<b>Step 1:</b> Select directory with your components:')
        path_label.setAlignment(Qt.AlignCenter)
        path_label.setContentsMargins(0,0,0,30)
        path_label.setFont(Lexend(self.title_font_size))

        self.path_input = QLineEditExtended()
        self.path_input.setMaximumWidth(int(0.5 * self.width))
        self.path_input.setMaximumHeight(50)
        self.path_input.setPlaceholderText('/path/to/directory')
        self.path_input.setFont(Lexend(self.status_font_size))
        self.path_input.clicked.connect(self.open_components_directory_dialog)
        self.path_input.textChanged.connect(self.update_path_input_status)

        path_input_layout = QtWidgets.QHBoxLayout()
        path_input_layout_widget = QtWidgets.QWidget()
        path_input_layout_widget.setLayout(path_input_layout)
        path_input_layout.setAlignment(Qt.AlignCenter)
        path_input_layout.addWidget(self.path_input)

        self.path_input_status = QtWidgets.QLabel()
        self.path_input_status.setText(f'<span style=\'color: {self.hint_color}\'>You need to fill this field!</span>')
        self.path_input_status.setAlignment(Qt.AlignCenter)
        self.path_input_status.setFont(Lexend(self.status_font_size))

        layers_order_label = QtWidgets.QLabel()
        layers_order_label.setText('<b>Step 2:</b> Select file with layers order:')
        layers_order_label.setAlignment(Qt.AlignCenter)
        layers_order_label.setContentsMargins(0,60,0,30)
        layers_order_label.setFont(Lexend(self.title_font_size))

        self.layers_order_input = QLineEditExtended()
        self.layers_order_input.setMaximumWidth(int(0.5 * self.width))
        self.layers_order_input.setMaximumHeight(50)
        self.layers_order_input.setPlaceholderText('/path/to/layers.json')
        self.layers_order_input.setFont(Lexend(self.status_font_size))
        self.layers_order_input.clicked.connect(self.open_layers_order_file_dialog)
        self.layers_order_input.textChanged.connect(self.update_layers_order_input_status)

        layers_order_input_layout = QtWidgets.QHBoxLayout()
        layers_order_input_layout_widget = QtWidgets.QWidget()
        layers_order_input_layout_widget.setLayout(layers_order_input_layout)
        layers_order_input_layout.setAlignment(Qt.AlignCenter)
        layers_order_input_layout.addWidget(self.layers_order_input)

        self.layers_order_input_status = QtWidgets.QLabel()
        self.layers_order_input_status.setText(f'<span style=\'color: {self.hint_color}\'>You need to fill this field!</span>')
        self.layers_order_input_status.setAlignment(Qt.AlignCenter)
        self.layers_order_input_status.setFont(Lexend(self.status_font_size))

        exceptions_label = QtWidgets.QLabel()
        exceptions_label.setText('<b>Step 3:</b> Select file with exceptions:')
        exceptions_label.setAlignment(Qt.AlignCenter)
        exceptions_label.setContentsMargins(0, 60, 0, 30)
        exceptions_label.setFont(Lexend(self.title_font_size))

        self.file_input = QLineEditExtended()
        self.file_input.setMaximumWidth(int(0.5 * self.width))
        self.file_input.setMaximumHeight(50)
        self.file_input.setPlaceholderText('/path/to/exceptions.json')
        self.file_input.setFont(Lexend(self.status_font_size))
        self.file_input.clicked.connect(self.open_exceptions_file_dialog)
        self.file_input.textChanged.connect(self.update_file_input_status)

        file_input_layout = QtWidgets.QHBoxLayout()
        file_input_layout_widget = QtWidgets.QWidget()
        file_input_layout_widget.setLayout(file_input_layout)
        file_input_layout.setAlignment(Qt.AlignCenter)
        file_input_layout.addWidget(self.file_input)

        self.file_input_status = QtWidgets.QLabel()
        self.file_input_status.setText(f'<span style=\'color: {self.hint_color}\'>(optional)</span>')
        self.file_input_status.setAlignment(Qt.AlignCenter)
        self.file_input_status.setFont(Lexend(self.status_font_size))

        rarity_label = QtWidgets.QLabel()
        rarity_label.setText('<b>Step 4:</b> Provide name of rarity files:')
        rarity_label.setAlignment(Qt.AlignCenter)
        rarity_label.setContentsMargins(0, 60, 0, 30)
        rarity_label.setFont(Lexend(self.title_font_size))

        self.rarity_input = QLineEditExtended()
        self.rarity_input.setMaximumWidth(int(0.5 * self.width))
        self.rarity_input.setMaximumHeight(50)
        self.rarity_input.setPlaceholderText('rarity.json')
        self.rarity_input.setFont(Lexend(self.status_font_size))
        self.rarity_input.textChanged.connect(self.update_rarity_input_status)

        rarity_input_layout = QtWidgets.QHBoxLayout()
        rarity_input_layout_widget = QtWidgets.QWidget()
        rarity_input_layout_widget.setLayout(rarity_input_layout)
        rarity_input_layout.setAlignment(Qt.AlignCenter)
        rarity_input_layout.addWidget(self.rarity_input)

        self.rarity_input_status = QtWidgets.QLabel()
        self.rarity_input_status.setText(f'<span style=\'color: {self.hint_color}\'>(optional)</span>')
        self.rarity_input_status.setAlignment(Qt.AlignCenter)
        self.rarity_input_status.setFont(Lexend(self.status_font_size))

        self.next_button = QtWidgets.QPushButton()
        self.next_button.setText('NEXT')
        self.next_button.setFixedWidth(int(0.2 * self.width))
        self.next_button.setMaximumHeight(80)
        self.next_button.setFont(Lexend(self.status_font_size))
        self.next_button.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.next_button.clicked.connect(self.next_button_function)
        self.activate_next_button()

        button_layout = QtWidgets.QHBoxLayout()
        button_widget = QtWidgets.QWidget()
        button_widget.setLayout(button_layout)
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setContentsMargins(0,50,0,0)
        button_layout.addWidget(self.next_button)

        self.path_layout.addWidget(path_label)
        self.path_layout.addWidget(path_input_layout_widget)
        self.path_layout.addWidget(self.path_input_status)
        self.path_layout.addWidget(layers_order_label)
        self.path_layout.addWidget(layers_order_input_layout_widget)
        self.path_layout.addWidget(self.layers_order_input_status)
        self.path_layout.addWidget(exceptions_label)
        self.path_layout.addWidget(file_input_layout_widget)
        self.path_layout.addWidget(self.file_input_status)
        self.path_layout.addWidget(rarity_label)
        self.path_layout.addWidget(rarity_input_layout_widget)
        self.path_layout.addWidget(self.rarity_input_status)

        self.path_layout.addWidget(button_widget)
        self.path_layout_widget.show()

        self.load_configuration()

    def create_interface(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout_widget = QtWidgets.QWidget()
        self.main_layout_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_layout_widget)

        self.info_layout = QtWidgets.QVBoxLayout()
        self.info_layout_widget = QtWidgets.QWidget()
        self.info_layout_widget.setLayout(self.info_layout)
        self.info_layout_widget.setMaximumHeight(int(0.4 * self.height))
        self.info_layout_widget.setObjectName('info-layout-widget')
        self.info_layout_widget.setStyleSheet('#info-layout-widget {border-bottom: 2px dashed #777;}')

        self.directories_layout = QtWidgets.QHBoxLayout()
        self.directories_layout_widget = QtWidgets.QWidget()
        self.directories_layout_widget.setLayout(self.directories_layout)

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setFixedSize(60, 30)
        self.back_button.move(10, 10)
        self.back_button.setIcon(QtGui.QIcon('img/back.svg'))
        icon_size = QtCore.QSize(30, 15)
        self.back_button.setIconSize(icon_size)
        self.back_button.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.back_button.clicked.connect(self.back_button_function)

        self.info_layout_hidden = False
        self.hide_button = QtWidgets.QPushButton(self)
        self.hide_button.setFixedSize(60, 30)
        self.hide_button.move(self.current_width() - self.hide_button.width() - 10, 10)
        self.hide_button.setText('Hide')
        self.hide_button.setFont(Lexend(self.status_font_size))
        self.hide_button.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.hide_button.clicked.connect(self.hide_info_layout)

        self.back_button.show()
        self.hide_button.show()

        self.available_directories_label = QtWidgets.QLabel()
        self.available_directories_label.setText('[Loading...]')
        self.available_directories_label.setAlignment(Qt.AlignCenter)
        self.available_directories_label.setFont(Lexend(self.info_font_size))

        self.info_labels = [QtWidgets.QLabel() for _ in range(4)]
        [label.setFont(Lexend(self.status_font_size)) for label in self.info_labels]
        [label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed) for label in self.info_labels]
        [label.setTextFormat(Qt.RichText) for label in self.info_labels] # Enforce HTML formatting

        self.summary_info = QtWidgets.QLabel()
        self.summary_info.setText('')
        self.summary_info.setAlignment(Qt.AlignCenter)
        self.summary_info.setFont(Lexend(self.status_font_size))
        self.summary_info.setContentsMargins(0,20,0,0)

        self.main_layout.addWidget(self.info_layout_widget)
        self.info_layout.addWidget(self.available_directories_label)
        self.info_layout.addWidget(self.directories_layout_widget)
        [self.directories_layout.addWidget(label) for label in self.info_labels]
        self.info_layout.addWidget(self.summary_info)

        self.image_generating_layout = QtWidgets.QVBoxLayout()
        self.image_generating_layout_widget = QtWidgets.QWidget()
        self.image_generating_layout_widget.setLayout(self.image_generating_layout)

        image_generating_mode_layout = QtWidgets.QHBoxLayout()
        image_generating_mode_layout_widget = QtWidgets.QWidget()
        image_generating_mode_layout_widget.setLayout(image_generating_mode_layout)
        image_generating_mode_layout.setAlignment(Qt.AlignCenter)
        image_generating_mode_layout.setSpacing(30)
        self.image_generating_layout.addWidget(image_generating_mode_layout_widget)

        generating_mode_label = QtWidgets.QLabel()
        generating_mode_label.setText('Select image generating mode:')
        generating_mode_label.setFont(Lexend(self.info_font_size))

        self.generating_mode_dropdown = QtWidgets.QComboBox()
        self.generating_mode_dropdown.addItems(['Manual', 'Automatic'])
        self.generating_mode_dropdown.setFont(Lexend(self.status_font_size))
        self.generating_mode_dropdown.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.generating_mode_dropdown.currentTextChanged.connect(self.update_generating_mode)

        image_generating_mode_layout.addWidget(generating_mode_label)
        image_generating_mode_layout.addWidget(self.generating_mode_dropdown)

        settings_label = QtWidgets.QLabel()
        settings_label.setText('Settings')
        settings_label.setFont(Lexend(self.info_font_size))
        settings_label.setAlignment(Qt.AlignCenter)
        settings_label.setContentsMargins(0,15,0,0)

        self.settings_layout = QtWidgets.QVBoxLayout()
        self.settings_layout_widget = QtWidgets.QWidget()
        self.settings_layout_widget.setLayout(self.settings_layout)

        options_label = QtWidgets.QLabel()
        options_label.setText('Options')
        options_label.setFont(Lexend(self.info_font_size))
        options_label.setAlignment(Qt.AlignCenter)
        options_label.setContentsMargins(0, 25, 0, 0)

        self.control_layout = QtWidgets.QHBoxLayout()
        self.control_layout_widget = QtWidgets.QWidget()
        self.control_layout_widget.setLayout(self.control_layout)
        self.control_layout.setAlignment(Qt.AlignCenter)
        self.control_layout.setSpacing(15)

        self.create_manual_generating_layout() # Because 'Manual' mode is default

        self.image_generating_layout.addWidget(settings_label)
        self.image_generating_layout.addWidget(self.settings_layout_widget)
        self.image_generating_layout.addWidget(options_label)
        self.image_generating_layout.addWidget(self.control_layout_widget)
        self.main_layout.addWidget(self.image_generating_layout_widget)

        self.result_layout = QtWidgets.QHBoxLayout()
        self.result_layout.setAlignment(Qt.AlignCenter)
        self.result_layout.setSpacing(30)
        self.result_layout.setContentsMargins(0,0,0,0)
        self.result_layout_widget = QWidgetExtended()
        self.result_layout_widget.resized.connect(self.resize_keeping_aspect_ratio)
        self.result_layout_widget.setLayout(self.result_layout)
        self.result_layout_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.generated_image_size = (1024, 1024)
        self.generated_image = QtWidgets.QLabel()
        self.generated_image.setMinimumSize(0, 0)
        self.generated_image.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.generated_image.setScaledContents(True) # Dynamically adjust pixmap to the size of the label
        self.generated_image.setStyleSheet('background-color: #777')

        self.traits_layout = QtWidgets.QVBoxLayout()
        self.traits_layout.setAlignment(Qt.AlignCenter)
        self.traits_layout.setContentsMargins(0,0,0,0)
        self.traits_layout_widget = QtWidgets.QWidget()
        self.traits_layout_widget.setLayout(self.traits_layout)
        self.traits_layout_widget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        traits_title_label = QtWidgets.QLabel()
        traits_title_label.setText('Traits:')
        traits_title_label.setFont(Lexend(self.info_font_size))
        traits_title_label.setAlignment(Qt.AlignCenter)

        self.traits_label = QtWidgets.QLabel()
        self.traits_label.setFont(Lexend(self.status_font_size))

        self.traits_layout.addWidget(traits_title_label)
        self.traits_layout.addWidget(self.traits_label)

        self.result_layout.addWidget(self.generated_image)
        self.result_layout.addWidget(self.traits_layout_widget)
        self.main_layout.addWidget(self.result_layout_widget)

    def resize_keeping_aspect_ratio(self):
        width, height = self.generated_image_size
        spacing = self.result_layout.spacing()
        ratio = width / height
        available_width = self.result_layout_widget.width() - self.traits_layout_widget.width() - spacing
        available_height = self.result_layout_widget.height()

        updated_height = available_height
        updated_width = int(updated_height * ratio)

        if updated_width <= available_width:
            # In this case height is the leading parameter
            if updated_width <= width and updated_height <= height:
                self.generated_image.setMaximumSize(updated_width, updated_height)
            else:
                self.generated_image.setMaximumSize(width, height)
        else:
            # In this case width is the leading parameter
            updated_width = available_width
            updated_height = int(updated_width / ratio)
            if updated_width <= width and updated_height <= height:
                self.generated_image.setMaximumSize(updated_width, updated_height)
            else:
                self.generated_image.setMaximumSize(width, height)

    def hide_info_layout(self):
        if not self.info_layout_hidden:
            self.info_layout_hidden = True
            self.info_layout_widget.hide()
            self.hide_button.setText('Show')

        else:
            self.info_layout_hidden = False
            self.info_layout_widget.show()
            self.hide_button.setText('Hide')

    def create_manual_generating_layout(self):
        self.clean_generating_mode_layouts()

        output_layout = QtWidgets.QHBoxLayout()
        output_layout_widget = QtWidgets.QWidget()
        output_layout_widget.setLayout(output_layout)
        output_layout.setAlignment(Qt.AlignCenter)
        output_layout.setSpacing(15)

        output_label = QtWidgets.QLabel()
        output_label.setText('Output path:')
        output_label.setFont(Lexend(self.status_font_size))
        output_label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.output_path_input = QLineEditExtended()
        self.output_path_input.setMaximumWidth(int(0.25 * self.width))
        self.output_path_input.setPlaceholderText('/path/to/output/directory')
        self.output_path_input.setFont(Lexend(self.status_font_size))
        self.output_path_input.clicked.connect(self.open_output_path_dialog)
        self.output_path_input.textChanged.connect(self.update_output_path_input)

        self.output_path_valid = QtWidgets.QLabel()

        output_layout.addWidget(QtWidgets.QWidget())
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_path_input)
        output_layout.addWidget(self.output_path_valid)
        self.settings_layout.addWidget(output_layout_widget)

        button_size = 100

        self.generate_button = QtWidgets.QPushButton()
        self.generate_button.setFixedWidth(button_size)
        self.generate_button.setText('Generate')
        self.generate_button.setFont(Lexend(self.status_font_size))
        self.generate_button.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.generate_button.clicked.connect(self.generate_image)

        self.save_button = QtWidgets.QPushButton()
        self.save_button.setFixedWidth(button_size)
        self.save_button.setText('Save')
        self.save_button.setFont(Lexend(self.status_font_size))
        self.save_button.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.save_button.clicked.connect(self.save_image)

        self.control_layout.addWidget(self.generate_button)
        self.control_layout.addWidget(self.save_button)

    def create_automatic_generating_layout(self):
        self.clean_generating_mode_layouts()
        label_width = 170

        output_layout = QtWidgets.QHBoxLayout()
        output_layout_widget = QtWidgets.QWidget()
        output_layout_widget.setLayout(output_layout)
        output_layout.setAlignment(Qt.AlignCenter)
        output_layout.setSpacing(15)

        output_label = QtWidgets.QLabel()
        output_label.setText('Output path:')
        output_label.setFont(Lexend(self.status_font_size))
        output_label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        output_label.setFixedWidth(label_width)

        self.output_path_input = QLineEditExtended()
        self.output_path_input.setMaximumWidth(int(0.25 * self.width))
        self.output_path_input.setPlaceholderText('/path/to/output/directory')
        self.output_path_input.setFont(Lexend(self.status_font_size))
        self.output_path_input.clicked.connect(self.open_output_path_dialog)
        self.output_path_input.textChanged.connect(self.update_output_path_input)

        self.output_path_valid = QtWidgets.QLabel()

        output_layout.addWidget(QtWidgets.QWidget())
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_path_input)
        output_layout.addWidget(self.output_path_valid)
        self.settings_layout.addWidget(output_layout_widget)

        time_delay_layout = QtWidgets.QHBoxLayout()
        time_delay_layout_widget = QtWidgets.QWidget()
        time_delay_layout_widget.setLayout(time_delay_layout)
        time_delay_layout.setAlignment(Qt.AlignCenter)
        time_delay_layout.setSpacing(15)

        time_delay_label = QtWidgets.QLabel()
        time_delay_label.setText('Time delay (seconds):')
        time_delay_label.setFont(Lexend(self.status_font_size))
        time_delay_label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        time_delay_label.setFixedWidth(label_width)

        self.time_delay_input = QLineEditDigitsOnly()
        self.time_delay_input.setFont(Lexend(self.status_font_size))
        self.time_delay_input.setMaximumWidth(int(0.25 * self.width))
        self.time_delay_input.textChanged.connect(self.update_time_delay_input)

        self.time_delay_valid = QtWidgets.QLabel()

        time_delay_layout.addWidget(QtWidgets.QWidget())
        time_delay_layout.addWidget(time_delay_label)
        time_delay_layout.addWidget(self.time_delay_input)
        time_delay_layout.addWidget(self.time_delay_valid)
        self.settings_layout.addWidget(time_delay_layout_widget)

        auto_save_layout = QtWidgets.QHBoxLayout()
        auto_save_layout_widget = QtWidgets.QWidget()
        auto_save_layout_widget.setLayout(auto_save_layout)
        auto_save_layout.setAlignment(Qt.AlignCenter)
        auto_save_layout.setSpacing(15)

        auto_save_label = QtWidgets.QLabel()
        auto_save_label.setText('Auto saving:')
        auto_save_label.setFont(Lexend(self.status_font_size))
        auto_save_label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.auto_save_dropdown = QtWidgets.QComboBox()
        self.auto_save_dropdown.addItems(['No', 'Yes'])
        self.auto_save_dropdown.setFont(Lexend(self.status_font_size))
        self.auto_save_dropdown.setCursor(QtGui.QCursor(Qt.PointingHandCursor))

        auto_save_layout.addWidget(auto_save_label)
        auto_save_layout.addWidget(self.auto_save_dropdown)
        self.settings_layout.addWidget(auto_save_layout_widget)

        button_size = 100

        self.start_button = QtWidgets.QPushButton()
        self.start_button.setFixedWidth(button_size)
        self.start_button.setFont(Lexend(self.status_font_size))
        self.start_button.setText('Start')
        self.start_button.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.start_button.clicked.connect(self.start_generating)

        self.stop_button = QtWidgets.QPushButton()
        self.stop_button.setFixedWidth(button_size)
        self.stop_button.setFont(Lexend(self.status_font_size))
        self.stop_button.setText('Stop')
        self.stop_button.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.stop_button.clicked.connect(self.stop_generating)

        self.save_button = QtWidgets.QPushButton()
        self.save_button.setFixedWidth(button_size)
        self.save_button.setText('Save')
        self.save_button.setFont(Lexend(self.status_font_size))
        self.save_button.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.save_button.clicked.connect(self.save_image)

        self.control_layout.addWidget(self.start_button)
        self.control_layout.addWidget(self.stop_button)
        self.control_layout.addWidget(self.save_button)

    def clean_generating_mode_layouts(self):
        for i in reversed(range(self.settings_layout.count())):
            widget = self.settings_layout.itemAt(i).widget()
            self.settings_layout.removeWidget(widget)
            widget.deleteLater()

        for i in reversed(range(self.control_layout.count())):
            widget = self.control_layout.itemAt(i).widget()
            self.control_layout.removeWidget(widget)
            widget.deleteLater()

    def open_components_directory_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.Option.DontUseNativeDialog
        dialog = QtWidgets.QFileDialog()
        dialog = dialog.getExistingDirectoryUrl(self, caption='Select directory with your components', options=options)
        self.path_input.setText(dialog.path())

    def open_layers_order_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.Option.DontUseNativeDialog
        dialog = QtWidgets.QFileDialog()
        dialog, _ = dialog.getOpenFileUrl(self, caption='Select JSON file with layers order', options=options)
        self.layers_order_input.setText(dialog.path())

    def open_exceptions_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.Option.DontUseNativeDialog
        dialog = QtWidgets.QFileDialog()
        dialog, _ = dialog.getOpenFileUrl(self, caption='Select JSON file with exceptions', options=options)
        self.file_input.setText(dialog.path())

    def open_output_path_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.Option.DontUseNativeDialog
        dialog = QtWidgets.QFileDialog()
        dialog = dialog.getExistingDirectoryUrl(self, caption='Select output path', options=options)
        self.output_path_input.setText(dialog.path())

    def get_valid_icon(self):
        pixmap = QtGui.QPixmap()
        pixmap.load('img/valid.svg')
        pixmap = pixmap.scaled(20, 20)
        return pixmap

    def get_invalid_icon(self):
        pixmap = QtGui.QPixmap()
        pixmap.load('img/invalid.svg')
        pixmap = pixmap.scaled(20, 20)
        return pixmap

    def next_button_function(self):
        self.mixer.components_path = self.path_input.text()
        self.mixer.layers_order_path = self.layers_order_input.text()
        self.mixer.exceptions_path = self.file_input.text()
        self.mixer.rarity_filename = self.rarity_input.text()

        self.path_layout_widget.deleteLater()
        self.create_interface()

        self.fetch_data_thread = FetchDataThread(self.mixer)
        self.fetch_data_thread.finished.connect(self.update_general_info)
        self.fetch_data_thread.finished.connect(self.update_traits_label)
        self.fetch_data_thread.imageSizeChanged.connect(self.update_image_area)
        self.fetch_data_thread.error.connect(self.display_error)
        self.fetch_data_thread.start()

        self.save_configuration()

    def back_button_function(self):
        self.main_layout_widget.deleteLater()
        self.initial_settings()

    def save_configuration(self):
        self.save_configuration_thread = SaveConfigurationThread(self.mixer)
        self.save_configuration_thread.start()

    def load_configuration(self):
        self.load_configuration_thread = LoadConfigurationThread()
        self.load_configuration_thread.finished.connect(self.update_input_fields)
        self.load_configuration_thread.start()

    def update_input_fields(self, data):
        self.path_input.setText(data.get('components_path'))
        self.layers_order_input.setText(data.get('layers_order_path'))
        self.file_input.setText(data.get('exceptions_path'))
        self.rarity_input.setText(data.get('rarity_filename'))

    def update_image_area(self):
        self.generated_image_size = self.mixer.image_size
        self.resize_keeping_aspect_ratio()

    def update_output_path_input(self):
        path = self.output_path_input.text()
        if os.path.isdir(path):
            self.output_path_valid.setPixmap(self.get_valid_icon())
        else:
            self.output_path_valid.setPixmap(self.get_invalid_icon())

    def update_time_delay_input(self):
        digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        text = self.time_delay_input.text()
        valid = True
        for char in text:
            if not char in digits:
                valid = False
                break
        if valid:
            self.time_delay_valid.setPixmap(self.get_valid_icon())
        else:
            self.time_delay_valid.setPixmap(self.get_invalid_icon())

    def update_path_input_status(self):
        self.path_input_valid = False
        path = self.path_input.text()
        if os.path.isdir(path):
            self.path_input_status.setText(f'<span style=\'color: {self.correct_color};\'>STATUS: Selected directory is correct!</span>')
            self.path_input_valid = True

        elif os.path.isfile(path):
            self.path_input_status.setText(f'<span style=\'color: {self.error_color};\'>ERROR: This field must contain a directory NOT a file!</span>')

        elif not path:
            self.path_input_status.setText(f'<span style=\'color: {self.error_color};\'>ERROR: You need to fill this field!</span>')

        else:
            self.path_input_status.setText(f'<span style=\'color: {self.error_color};\'>ERROR: This path does NOT exist!</span>')

        self.activate_next_button()

    def update_layers_order_input_status(self):
        self.layers_order_input_valid = False
        path = self.layers_order_input.text()
        if os.path.isfile(path):
            self.layers_order_input_status.setText(f'<span style=\'color: {self.correct_color};\'>STATUS: Layers order file is correct!</span>')
            self.layers_order_input_valid = True

        elif os.path.isdir(path):
            self.layers_order_input_status.setText(f'<span style=\'color: {self.error_color};\'>ERROR: This field must contain a file NOT a directory!</span>')

        elif not path:
            self.layers_order_input_status.setText(f'<span style=\'color: {self.error_color};\'>ERROR: You need to fill this field!</span>')

        else:
            self.layers_order_input_status.setText(f'<span style=\'color: {self.error_color};\'>ERROR: This file does NOT exist!</span>')

        self.activate_next_button()

    def update_file_input_status(self):
        self.file_input_valid = False
        path = self.file_input.text()
        if os.path.isfile(path):
            if path.split('.')[-1].lower() == 'json':
                self.file_input_status.setText(f'<span style=\'color: {self.correct_color};\'>STATUS: Exceptions file is correct!</span>')
                self.file_input_valid = True
            else:
                self.file_input_status.setText(f'<span style=\'color: {self.error_color};\'>ERROR: File\'s extension is invalid! Only JSON files are accepted.</span>')

        elif os.path.isdir(path):
            self.file_input_status.setText(f'<span style=\'color: {self.error_color};\'>ERROR: This field must contain a file NOT a directory!</span>')

        elif not path:
            self.file_input_status.setText(f'<span style=\'color: {self.warning_color};\'>WARNING: Leaving this field empty means that all combinations are allowed!</span>')
            self.file_input_valid = True

        else:
            self.file_input_status.setText(f'<span style=\'color: {self.error_color};\'>ERROR: This file does NOT exist!</span>')

        self.activate_next_button()

    def update_rarity_input_status(self):
        self.rarity_input_valid = False
        text = self.rarity_input.text()
        if text:
            if text.split('.')[-1].lower() == 'json':
                self.rarity_input_status.setText(f'<span style=\'color: {self.correct_color};\'>STATUS: Provided name is correct!</span>')
                self.rarity_input_valid = True
            else:
                self.rarity_input_status.setText(f'<span style=\'color: {self.error_color};\'>ERROR: Only JSON files are accepted!</span>')

        else:
            self.rarity_input_status.setText(f'<span style=\'color: {self.warning_color};\'>WARNING: Leaving this field empty means that all of your items have equal rarity!</span>')
            self.rarity_input_valid = True

        self.activate_next_button()

    def activate_next_button(self):
        if self.path_input_valid and self.layers_order_input_valid and self.file_input_valid and self.rarity_input_valid:
            self.next_button.setDisabled(False)
        else:
            self.next_button.setDisabled(True)

    def update_info_labels(self, data):
        index = -1
        rows = len(data) // 4 + 1 if len(data) % 4 else len(data) // 4
        for label in self.info_labels:
            content = ''
            for i in range(rows):
                index += 1
                if index >= len(data):
                    break
                content += data[index]
                if i != rows - 1:
                    content += '<br>'
            label.setText(content)

    def update_traits_label(self):
        text = ''
        for trait in self.mixer.data:
            text += f'{trait}: {self.mixer.current_traits.get(trait, "---")}<br>'
        text = text[:-4] # Cut out last <br> tag
        self.traits_label.setText(text)

    def update_general_info(self):
        non_empty_dirs = 0
        for img_list in self.mixer.data.values():
            if img_list:
                non_empty_dirs += 1

        if not self.mixer.data:
            self.available_directories_label.setText(f'<span style=\'color: {self.error_color}\'>There are no directories on the path! Go back and select new path.</span>')
            self.disable_generating_controls(True)
        elif non_empty_dirs == len(self.mixer.data):
            self.available_directories_label.setText(f'Available directories: <b>{non_empty_dirs}</b>')
            self.disable_generating_controls(False)
        elif non_empty_dirs > 0:
            excluded = len(self.mixer.data)-non_empty_dirs
            self.available_directories_label.setText(f'Available directories: <b>{non_empty_dirs}</b><br><span style=\'color: {self.warning_color}\'>({excluded} {"were" if excluded>1 else "was"} excluded)</span>')
            self.disable_generating_controls(False)
        else:
            self.available_directories_label.setText(f'<span style=\'color: {self.error_color}\'>All directories are empty! Go back and select new path.</span>')
            self.disable_generating_controls(True)

        if len(self.mixer.skipped_data) > 1:
            text = self.available_directories_label.text()
            self.available_directories_label.setText(text + f'<br><span style=\'color: {self.warning_color}\'>({len(self.mixer.skipped_data)} weren\'t listed in layers order)</span>') # For plural form
        elif len(self.mixer.skipped_data) == 1:
            text = self.available_directories_label.text()
            self.available_directories_label.setText(text + f'<br><span style=\'color: {self.warning_color}\'>({len(self.mixer.skipped_data)} wasn\'t listed in layers order)</span>') # For singular form

        if self.mixer.data:
            dirs = sorted(list(self.mixer.data.keys()) + list(self.mixer.skipped_data.keys()), key=lambda x: x.lower())
            formatted_dirs = []
            for i in range(len(dirs)):
                if dirs[i] in self.mixer.data:
                    images = len(self.mixer.data[dirs[i]])
                    formatted_dir = f'{i+1}. {dirs[i]} ({images})'
                    if not images:
                        formatted_dir = f'<span style=\'color: {self.warning_color}\'>{formatted_dir}</span>'
                else:
                    images = len(self.mixer.skipped_data[dirs[i]])
                    formatted_dir = f'<span style=\'color: {self.hint_color}; text-decoration: line-through;\'>{i + 1}. {dirs[i]} ({images})</span>'

                formatted_dirs.append(formatted_dir)

            self.update_info_labels(formatted_dirs)

            self.summary_info.setText(
                f'Total images: <b>{self.readable_number(self.mixer.total_images)}</b><br>'
                f'Total possible combinations: <b>{self.readable_number(self.mixer.possible_combinations)}</b><br>'
            )

    def update_generating_mode(self):
        mode = self.generating_mode_dropdown.currentText()
        if mode == 'Manual':
            self.create_manual_generating_layout()
        elif mode == 'Automatic':
            self.create_automatic_generating_layout()

    def disable_generating_controls(self, state):
        try:
            self.generating_mode_dropdown.setDisabled(state)
            self.generate_button.setDisabled(state)
            self.save_button.setDisabled(state)
        except:
            pass
        try:
            self.start_button.setDisabled(state)
            self.stop_button.setDisabled(state)
            self.save_button.setDisabled(state)
        except:
            pass

    def display_error(self, message):
        self.available_directories_label.setText(f'<span style=\'color: {self.error_color}\'>{message}</span>')
        self.disable_generating_controls(True)

    def update_generated_image(self, image):
        image = QtGui.QImage(image.tobytes('raw', 'RGBA'), *self.generated_image_size, QtGui.QImage.Format_RGBA8888)
        pixmap = QtGui.QPixmap()
        pixmap = pixmap.fromImage(image)
        self.generated_image.setPixmap(pixmap)
        self.generated_image.setMinimumSize(1, 1)
        self.update_traits_label()

    def generate_image(self):
        self.generate_image_thread = GenerateImageThread(self.mixer)
        self.generate_image_thread.finished.connect(self.update_generated_image)
        self.generate_image_thread.start()

    def save_image(self):
        print('Image saved successfully!')

    def start_generating(self):
        print('Generating started!')

    def stop_generating(self):
        print('Generating stopped!')

    def readable_number(self, n):
        n = list(reversed(str(n)))
        group = ''
        result = []
        for i in range(len(n)):
            group += str(n[i])
            if not (i + 1) % 3:
                result.append(group)
                group = ''
            if i == len(n) - 1:
                result.append(group)
        return ''.join(list(reversed(' '.join(result)))).strip()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        try:
            self.hide_button.move(self.current_width() - self.hide_button.width() - 10, 10) # Update position of hide_button when main window is resized
        except:
            pass


class FetchDataThread(QtCore.QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    imageSizeChanged = pyqtSignal()
    def __init__(self, mixer):
        super().__init__()
        self.mixer = mixer

    def run(self):
        try:
            self.mixer.fetch_data()
        except ComponentsPathError:
            self.error.emit('Error while reading components path!')
        except LayersOrderFileError:
            self.error.emit('Error with layers order file!')
        except ExceptionsFileError:
            self.error.emit('Error with exceptions file!')
        except RarityFileError:
            self.error.emit('Error in one of rarity files!')
        else:
            self.finished.emit()
            self.imageSizeChanged.emit()

class GenerateImageThread(QtCore.QThread):
    finished = pyqtSignal(object)
    def __init__(self, mixer):
        super().__init__()
        self.mixer = mixer

    def run(self):
        image = self.mixer.generate()
        self.finished.emit(image)

class SaveConfigurationThread(QtCore.QThread):
    def __init__(self, mixer):
        super().__init__()
        self.mixer = mixer

    def run(self):
        data = {
            'components_path': self.mixer.components_path,
            'layers_order_path': self.mixer.layers_order_path,
            'exceptions_path': self.mixer.exceptions_path,
            'rarity_filename': self.mixer.rarity_filename
        }
        data = json.dumps(data)
        with open(os.getcwd() + '/config.json', 'w') as conf:
            conf.write(data)

class LoadConfigurationThread(QtCore.QThread):
    finished = pyqtSignal(dict)
    def run(self):
        if os.path.isfile(os.getcwd() + '/config.json'):
            try:
                with open(os.getcwd() + '/config.json', 'r') as conf:
                    data = conf.read()
                data = json.loads(data)
                self.finished.emit(data)
            except:
                pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec_())