import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QLineEdit, QTextEdit
from PyQt5.QtGui import QColor, QIcon, QTextCursor
import subprocess
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("traiNNer GUI")
        self.setStyleSheet("background-color: #333333; color: #FFFFFF;")
        self.setFixedSize(400, 300)
        self.setWindowIcon(QIcon("trainner.png"))
        self.init_ui()

    def init_ui(self):
        self.label = QLabel("Select YML options config:", self)
        self.label.setGeometry(20, 20, 250, 25)
        self.label.setStyleSheet("margin-right: 10px;")

        self.btn_select_files = QPushButton("Select Files", self)
        self.btn_select_files.move(20, 50)
        self.btn_select_files.setStyleSheet("background-color: #555555; color: #FFFFFF;")
        self.btn_select_files.clicked.connect(self.select_files)

        self.selected_file_text = QLineEdit(self)
        self.selected_file_text.setReadOnly(True)
        self.selected_file_text.setGeometry(150, 50, 230, 25)
        self.selected_file_text.setStyleSheet("background-color: #444444; color: #FFFFFF;")

        self.btn_train = QPushButton("Train", self)
        self.btn_train.move(20, 100)
        self.btn_train.setStyleSheet("background-color: #555555; color: #FFFFFF;")
        self.btn_train.clicked.connect(self.start_training)

        self.btn_stop_train = QPushButton("Stop Training", self)
        self.btn_stop_train.move(120, 100)
        self.btn_stop_train.setStyleSheet("background-color: #555555; color: #FFFFFF;")
        self.btn_stop_train.clicked.connect(self.stop_training)
        self.btn_stop_train.setEnabled(False)

        self.console_output = QTextEdit(self)
        self.console_output.setGeometry(20, 150, 360, 120)
        self.console_output.setStyleSheet("background-color: #111111; color: #FFFFFF;")
        self.console_output.setReadOnly(True)

        sys.stdout = ConsoleWriter(self.console_output)

    def select_files(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("YAML files (*.yml)")
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.input_file = selected_files[0]
                self.selected_file_text.setText(self.input_file)

    def start_training(self):
        if hasattr(self, 'input_file'):
            print(f"Training started with file: {self.input_file}")
            script_dir = os.path.dirname(os.path.realpath(__file__))
            train_script = os.path.join(script_dir, "train.py")
            self.process = subprocess.Popen(["python", train_script, "-opt", self.input_file], stdout=subprocess.PIPE, universal_newlines=True)
            self.btn_train.setEnabled(False)
            self.btn_stop_train.setEnabled(True)
            self.btn_stop_train.setStyleSheet("background-color: #FF5555; color: #FFFFFF;")
        else:
            print("Please select input files before training!")

    def stop_training(self):
        if hasattr(self, 'process'):
            self.process.terminate()
            print("Training process stopped.")
            self.btn_train.setEnabled(True)
            self.btn_stop_train.setEnabled(False)
            self.btn_stop_train.setStyleSheet("background-color: #555555; color: #FFFFFF;")
        else:
            print("No training process running.")

class ConsoleWriter:
    def __init__(self, console_output):
        self.console_output = console_output

    def write(self, message):
        self.console_output.moveCursor(QTextCursor.End)
        self.console_output.ensureCursorVisible()
        self.console_output.insertPlainText(message)

    def flush(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    dark_palette = app.palette()
    dark_palette.setColor(dark_palette.Window, QColor(53, 53, 53))
    dark_palette.setColor(dark_palette.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(dark_palette.Base, QColor(25, 25, 25))
    dark_palette.setColor(dark_palette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(dark_palette.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(dark_palette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(dark_palette.Text, QColor(255, 255, 255))
    dark_palette.setColor(dark_palette.Button, QColor(53, 53, 53))
    dark_palette.setColor(dark_palette.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(dark_palette.BrightText, QColor(255, 255, 255))
    dark_palette.setColor(dark_palette.Highlight, QColor(42, 110, 184))
    dark_palette.setColor(dark_palette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(dark_palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
