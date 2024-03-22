import sys

from PyQt5.QtWidgets import QApplication
from ui.LoginWindow import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #main_window = MainWindow()
    login_window = LoginWindow()

    login_window.show()
    #main_window.show()
    app.exec_()
