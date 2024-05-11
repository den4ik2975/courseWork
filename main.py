import sys

from PyQt5.QtWidgets import QApplication

from src.ui.LoginWindow import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()

    login_window.show()
    app.exec_()
