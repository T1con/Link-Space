import sys
from PyQt6.QtWidgets import QApplication
from src.LoginWindow import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load stylesheet
    try:
        with open("src/style.qss", "r") as f:
            style = f.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("Stylesheet not found. Using default styles.")

    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
