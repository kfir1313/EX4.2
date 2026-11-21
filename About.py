from pathlib import Path
import webbrowser

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QPushButton,
    QWidget,
)

BASE_DIR = Path(__file__).resolve().parent


class AboutWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("About Me")
        self.setGeometry(100, 100, 404, 500)
        self.setFixedSize(404, 500)
        self.setStyleSheet("""
            background-color: #0b1220;
            color: #e2e8f0;
            font-family: "Segoe UI";
        """)

        card = QFrame(self)
        card.setGeometry(24, 24, 356, 452)
        card.setStyleSheet("""
            background-color: #111c2e;
            border-radius: 18px;
        """)

        eyebrow = QLabel(">>> ABOUT / DEVELOPER", card)
        eyebrow.setGeometry(28, 22, 300, 20)
        eyebrow.setStyleSheet("""
            color: #67e8f9;
            font-family: Consolas;
            font-size: 12px;
            font-weight: 600;
        """)

        name = QLabel("Kfir Frenkel", card)
        name.setGeometry(28, 52, 300, 40)
        name.setStyleSheet("""
            color: #f8fafc;
            font-size: 30px;
            font-weight: 700;
        """)

        intro = QLabel("I enjoy bringing ideas to life", card)
        intro.setGeometry(28, 98, 300, 24)
        intro.setStyleSheet("""
            color: #9fb0c6;
            font-size: 14px;
        """)

        self.my_picture = QLabel(card)
        self.my_picture.setPixmap(QPixmap(str(BASE_DIR / "me.jpeg")).scaled(300, 150))
        self.my_picture.setGeometry(28, 134, 300, 150)
        self.my_picture.setStyleSheet(
            "background-color: #17263b; border-radius: 10px;"
        )

        divider = QFrame(card)
        divider.setGeometry(28, 304, 300, 1)
        divider.setStyleSheet("""
            background-color: #22314a;
            max-height: 1px;
        """)

        contact_label = QLabel("GET IN TOUCH", card)
        contact_label.setGeometry(28, 326, 300, 18)
        contact_label.setStyleSheet("""
            color: #71839d;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1px;
        """)

        self.mail = QLabel("kfir.frenkel@gmail.com", card)
        self.mail.setGeometry(28, 362, 240, 40)
        self.mail.setStyleSheet("""
            color: #d7e1ef;
            font-size: 13px;
        """)

        self.linkedin_button = QPushButton(card)
        logo = QPixmap(str(BASE_DIR / "linkedin.svg"))
        self.linkedin_button.setIcon(QIcon(logo))
        self.linkedin_button.setIconSize(QSize(24, 24))
        self.linkedin_button.setGeometry(288, 362, 40, 40)
        self.linkedin_button.setStyleSheet("""
            QPushButton {
                background-color: #172a43;
                border-radius: 8px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #203b5a;
            }
            QPushButton:pressed {
                background-color: #12243a;
            }
        """)
        self.linkedin_button.setToolTip("Open LinkedIn profile")
        self.linkedin_button.clicked.connect(self._open_linkedin)

    def _open_linkedin(self):
        webbrowser.open("https://www.linkedin.com/in/kfir-frenkel-9b987a229/")


if __name__ == "__main__":
    app = QApplication()
    window = AboutWindow()
    window.show()
    app.exec()
