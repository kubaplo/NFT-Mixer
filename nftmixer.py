import sys, os
from PyQt5 import QtWidgets, QtGui
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


        def next():
            self.path_layout_widget.deleteLater()
            self.create_interface()

        self.next_button = QtWidgets.QPushButton()
        self.next_button.setText('NEXT')
        self.next_button.setFixedWidth(int(0.2 * self.width))
        self.next_button.setMaximumHeight(80)
        self.next_button.setFont(Lexend(self.status_font_size))
        self.next_button.clicked.connect(next)
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


    def create_interface(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout_widget = QtWidgets.QWidget()
        self.main_layout_widget.setLayout(self.main_layout)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout_widget.setStyleSheet('background-color: red') #debug

        self.info_layout = QtWidgets.QVBoxLayout()
        self.info_layout_widget = QtWidgets.QWidget()
        self.info_layout_widget.setLayout(self.info_layout)
        self.info_layout_widget.setMaximumHeight(int(0.4 * self.height))
        self.info_layout_widget.setStyleSheet('background-color: blue') #debug

        self.directories_layout = QtWidgets.QHBoxLayout()
        self.directories_layout_widget = QtWidgets.QWidget()
        self.directories_layout_widget.setLayout(self.directories_layout)
        self.directories_layout_widget.setStyleSheet('background-color: yellow') #debug

        self.available_directories_label = QtWidgets.QLabel()
        self.available_directories_label.setText('Available directories: 14')
        self.available_directories_label.setAlignment(Qt.AlignCenter)
        self.available_directories_label.setStyleSheet('background-color: green') #debug
        self.available_directories_label.setFont(Lexend(self.info_font_size))

        self.info_labels = [QtWidgets.QLabel() for _ in range(4)]
        [label.setFont(Lexend(self.status_font_size)) for label in self.info_labels]
        data = ['1. tttasfjalkfjsdafj', '2. adjflasdjflasdj', '3. adsjflkasdjflsdajflsadkj', '4. ajflajdslfjfljasdlfj', '5. asldfjalsjflasjfsa', '6. adlfjaslfjalsfjalsjflsa', '7. lkjdasfoelkmvda;f', '8. la;jf;lajfljfljsadlfk', '9. jflaksjfl', '10. jaslfjldksfjakls;dfj', '11. dadsfasd', '12. adfsdfsd', '13. afasdf', '14. askjfaksldjf']

        index = -1
        rows = len(data)//4+1 if len(data)%4 else len(data)//4
        for label in self.info_labels:
            content = ''
            for i in range(rows):
                index += 1
                if index == len(data):
                    break
                content += data[index]
                if i != rows-1:
                    content += '\n'
            label.setText(content)

        self.summary_info = QtWidgets.QLabel()
        self.summary_info.setText('Total items: 50\nPossible combinations: 12 500')
        self.summary_info.setStyleSheet('background-color: green') #debug
        self.summary_info.setAlignment(Qt.AlignCenter)
        self.summary_info.setFont(Lexend(self.status_font_size))

        self.setCentralWidget(self.main_layout_widget)
        self.main_layout.addWidget(self.info_layout_widget)
        self.info_layout.addWidget(self.available_directories_label)
        self.info_layout.addWidget(self.directories_layout_widget)
        [self.directories_layout.addWidget(label) for label in self.info_labels]
        [label.setStyleSheet('background-color: green;') for label in self.info_labels]
        self.info_layout.addWidget(self.summary_info)

        self.main_layout_widget.show()
        self.info_layout_widget.show()



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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec_())