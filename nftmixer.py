import sys, os, json
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow

'''sys._excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = exception_hook'''

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


class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('NFTs Mixer')
        self.screen_width = QApplication.primaryScreen().size().width()
        self.screen_height = QApplication.primaryScreen().size().height()
        self.width = int(0.5 * self.screen_width)
        self.height = int(0.7 * self.screen_height)
        self.setGeometry(int((self.screen_width-self.width)/2), int((self.screen_height-self.height)/2), self.width, self.height)
        self.setStyleSheet('background-color: #888;')
        self.define_constants()
        self.initial_settings()

    def define_constants(self):
        self.title_font_size = 20
        self.status_font_size = 12
        self.info_font_size = 14
        self.error_color = '#c91414'
        self.warning_color = '#fa0'
        self.correct_color = '#62ff00'
        self.path_input_valid = False
        self.file_input_valid = True
        self.rarity_input_valid = True
        self.directory_path = ''
        self.exceptions_path = ''
        self.rarity_filename = ''
        self.data = {}


    def initial_settings(self):
        self.path_layout = QtWidgets.QVBoxLayout()
        self.path_layout_widget = QtWidgets.QWidget()
        self.path_layout_widget.setLayout(self.path_layout)
        self.path_layout.setAlignment(Qt.AlignCenter)

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
        self.path_input_status.setText('')
        self.path_input_status.setAlignment(Qt.AlignCenter)
        self.path_input_status.setFont(Lexend(self.status_font_size))

        exceptions_label = QtWidgets.QLabel()
        exceptions_label.setText('<b>Step 2:</b> Select file with exceptions:')
        exceptions_label.setAlignment(Qt.AlignCenter)
        exceptions_label.setContentsMargins(0, 70, 0, 30)
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
        self.file_input_status.setText('')
        self.file_input_status.setAlignment(Qt.AlignCenter)
        self.file_input_status.setFont(Lexend(self.status_font_size))

        rarity_label = QtWidgets.QLabel()
        rarity_label.setText('<b>Step 3:</b> Provide name of rarity files:')
        rarity_label.setAlignment(Qt.AlignCenter)
        rarity_label.setContentsMargins(0, 70, 0, 30)
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
        self.rarity_input_status.setText('')
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

        self.setCentralWidget(self.path_layout_widget)
        self.path_layout.addWidget(path_label)
        self.path_layout.addWidget(path_input_layout_widget)
        self.path_layout.addWidget(self.path_input_status)
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

        self.info_layout = QtWidgets.QVBoxLayout()
        self.info_layout_widget = QtWidgets.QWidget()
        self.info_layout_widget.setLayout(self.info_layout)
        self.info_layout_widget.setMaximumHeight(int(0.4 * self.height))
        self.info_layout_widget.setObjectName('info-layout-widget')
        self.info_layout_widget.setStyleSheet('#info-layout-widget {border-bottom: 2px dashed #777;}')

        self.directories_layout = QtWidgets.QHBoxLayout()
        self.directories_layout_widget = QtWidgets.QWidget()
        self.directories_layout_widget.setLayout(self.directories_layout)

        top_bar_layout = QtWidgets.QHBoxLayout()
        top_bar_layout_widget = QtWidgets.QWidget()
        top_bar_layout_widget.setLayout(top_bar_layout)
        top_bar_layout.setContentsMargins(0,0,0,0)

        self.back_button = QtWidgets.QPushButton()
        self.back_button.setFixedSize(60, 30)
        self.back_button.setIcon(QtGui.QIcon('img/back.svg'))
        icon_size = QtCore.QSize(30, 15)
        self.back_button.setIconSize(icon_size)
        self.back_button.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.back_button.clicked.connect(self.back_button_function)

        centering_help = QtWidgets.QWidget()
        centering_help.setFixedSize(60, 30)

        self.available_directories_label = QtWidgets.QLabel()
        self.available_directories_label.setText('')
        self.available_directories_label.setAlignment(Qt.AlignCenter)
        self.available_directories_label.setFont(Lexend(self.info_font_size))

        top_bar_layout.addWidget(self.back_button)
        top_bar_layout.addWidget(self.available_directories_label)
        top_bar_layout.addWidget(centering_help)

        self.info_labels = [QtWidgets.QLabel() for _ in range(4)]
        [label.setFont(Lexend(self.status_font_size)) for label in self.info_labels]
        [label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed) for label in self.info_labels]

        self.summary_info = QtWidgets.QLabel()
        self.summary_info.setText('')
        self.summary_info.setAlignment(Qt.AlignCenter)
        self.summary_info.setFont(Lexend(self.status_font_size))
        self.summary_info.setContentsMargins(0,20,0,0)

        self.setCentralWidget(self.main_layout_widget)
        self.main_layout.addWidget(self.info_layout_widget)
        self.info_layout.addWidget(top_bar_layout_widget)
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
        self.output_path_input.clicked.connect(self.open_output_path_dialog)
        self.output_path_input.textChanged.connect(self.update_output_path_input)

        self.output_path_valid = QtWidgets.QLabel()

        output_layout.addWidget(QtWidgets.QWidget())
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_path_input)
        output_layout.addWidget(self.output_path_valid)
        self.settings_layout.addWidget(output_layout_widget)

        buttons_size = 100

        self.generate_button = QtWidgets.QPushButton()
        self.generate_button.setFixedWidth(buttons_size)
        self.generate_button.setText('Generate')
        self.generate_button.setFont(Lexend(self.status_font_size))
        self.generate_button.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.generate_button.clicked.connect(self.generate_image)

        self.save_button = QtWidgets.QPushButton()
        self.save_button.setFixedWidth(buttons_size)
        self.save_button.setText('Save')
        self.save_button.setFont(Lexend(self.status_font_size))
        self.save_button.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.save_button.clicked.connect(self.save_image)

        self.control_layout.addWidget(self.generate_button)
        self.control_layout.addWidget(self.save_button)


    def create_automatic_generating_layout(self):
        self.clean_generating_mode_layouts()

    def clean_generating_mode_layouts(self):
        index = self.settings_layout.count() - 1
        for i in range(index + 1):
            index -= i
            self.settings_layout.itemAt(index).widget().deleteLater()

        index = self.control_layout.count() - 1
        for i in range(index + 1):
            index -= i
            self.control_layout.itemAt(index).widget().deleteLater()






    def open_components_directory_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.Option.DontUseNativeDialog
        self.dialog = QtWidgets.QFileDialog()
        self.dialog = self.dialog.getExistingDirectoryUrl(self, caption='Select directory with your components', options=options)
        self.path_input.setText(self.dialog.path())

    def open_exceptions_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.Option.DontUseNativeDialog
        self.dialog = QtWidgets.QFileDialog()
        self.dialog, _ = self.dialog.getOpenFileUrl(self, caption='Select JSON file with exceptions', options=options)
        self.file_input.setText(self.dialog.path())

    def open_output_path_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.Option.DontUseNativeDialog
        self.dialog = QtWidgets.QFileDialog()
        self.dialog = self.dialog.getExistingDirectoryUrl(self, caption='Select output path', options=options)
        self.output_path_input.setText(self.dialog.path())

    def get_valid_icon(self):
        pixmap = QtGui.QPixmap()
        pixmap.load('img/valid.svg')
        pixmap = pixmap.scaled(20,20)
        return pixmap

    def get_invalid_icon(self):
        pixmap = QtGui.QPixmap()
        pixmap.load('img/invalid.svg')
        pixmap = pixmap.scaled(20, 20)
        return pixmap

    def next_button_function(self):
        self.directory_path = self.path_input.text()
        self.exceptions_path = self.file_input.text()
        self.rarity_filename = self.rarity_input.text()
        self.build_data()
        self.path_layout_widget.deleteLater()
        self.create_interface()
        self.update_general_info()
        self.save_configuration()

    def back_button_function(self):
        self.main_layout_widget.deleteLater()
        self.initial_settings()

    def save_configuration(self):
        data = {
            'directory_path': self.directory_path,
            'exceptions_path': self.exceptions_path,
            'rarity_filename': self.rarity_filename
        }
        data = json.dumps(data)
        with open(os.getcwd() + '/config.json', 'w') as conf:
            conf.write(data)

    def load_configuration(self):
        if os.path.isfile(os.getcwd() + '/config.json'):
            try:
                with open(os.getcwd() + '/config.json', 'r') as conf:
                    data = conf.read()
                data = json.loads(data)

                self.path_input.setText(data.get('directory_path'))
                self.file_input.setText(data.get('exceptions_path'))
                self.rarity_input.setText(data.get('rarity_filename'))
            except:
                pass

    def update_output_path_input(self):
        path = self.output_path_input.text()
        if os.path.isdir(path):
            self.output_path_valid.setPixmap(self.get_valid_icon())
        else:
            self.output_path_valid.setPixmap(self.get_invalid_icon())

    def update_path_input_status(self):
        self.path_input_valid = False
        path = self.path_input.text()
        if os.path.isdir(path):
            dirs = 0
            images = 0
            with os.scandir(path) as scan:
                for file in scan:
                    if file.is_dir():
                        dirs += 1
                        with os.scandir(file.path) as subscan:
                            for subfile in subscan:
                                if subfile.is_file() and subfile.name.split('.')[-1].lower() == 'png':
                                    images += 1

            if dirs:
                if images:
                    self.path_input_status.setText(f'<span style=\'color: {self.correct_color};\'>STATUS: Provided directory is correct! It contains {dirs} subdirectories & {images} PNG images!</span>')
                    self.path_input_valid = True
                else:
                    self.path_input_status.setText(f'<span style=\'color: {self.error_color};\'>ERROR: Subdirectories within this directory do NOT contain any PNG images!</span>')
            else:
                self.path_input_status.setText(f'<span style=\'color: {self.error_color};\'>ERROR: This directory is empty!</span>')

        elif os.path.isfile(path):
            self.path_input_status.setText(f'<span style=\'color: {self.error_color};\'>ERROR: This field must contain a directory NOT a file!</span>')

        elif not path:
            self.path_input_status.setText(f'<span style=\'color: {self.error_color};\'>ERROR: You need to fill this field!</span>')

        else:
            self.path_input_status.setText(f'<span style=\'color: {self.error_color};\'>ERROR: This path does NOT exist!</span>')

        self.activate_next_button()

    def update_file_input_status(self):
        self.file_input_valid = False
        path = self.file_input.text()
        if os.path.isfile(path):
            if path.split('.')[-1].lower() == 'json':
                self.file_input_status.setText(f'<span style=\'color: {self.correct_color};\'>STATUS: Provided exceptions file is correct!</span>')
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
        if self.path_input_valid and self.file_input_valid and self.rarity_input_valid:
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
                if index == len(data):
                    break
                content += data[index]
                if i != rows - 1:
                    content += '\n'
            label.setText(content)

    def build_data(self):
        #TODO: Decide whether leave this method here or move to backend file.
        self.data = {}
        with os.scandir(self.directory_path) as scan:
            for file in scan:
                if file.is_dir():
                    self.data[file.name] = []
                    with os.scandir(file.path) as subscan:
                        for subfile in subscan:
                            if subfile.is_file() and subfile.name.split('.')[-1].lower() == 'png':
                                self.data[file.name].append(subfile.name)

    def update_general_info(self):
        self.available_directories_label.setText(f'Available directories: <b>{len(self.data)}</b>')

        dirs = sorted(self.data.keys())
        self.update_info_labels([f'{i + 1}. {dirs[i]}' for i in range(len(dirs))])

        total_images = 0
        possible_combinations = 1
        for x in self.data.values():
            total_images += len(x)
            possible_combinations *= len(x)

        self.summary_info.setText(
            f'Total images: <b>{self.readable_number(total_images)}</b><br>'
            f'Total possible combinations: <b>{self.readable_number(possible_combinations)}</b><br>'
        )

    def update_generating_mode(self):
        mode = self.generating_mode_dropdown.currentText()
        if mode == 'Manual':
            self.create_manual_generating_layout()
        elif mode == 'Automatic':
            self.create_automatic_generating_layout()

    def generate_image(self):
        print('Image generated successfully!')

    def save_image(self):
        print('Image saved successfully!')

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec_())