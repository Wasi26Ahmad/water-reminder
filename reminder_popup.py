from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout
)


class ReminderPopup(QDialog):
    def __init__(self, message):
        super().__init__()

        self.setWindowTitle("Reminder")
        self.setModal(True)

        self.setWindowFlag(
            Qt.WindowType.WindowStaysOnTopHint,
            True
        )

        self.resize(300, 150)

        layout = QVBoxLayout()

        label = QLabel(message)
        label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        button = QPushButton("Done")
        button.clicked.connect(self.accept)

        layout.addWidget(label)
        layout.addWidget(button)

        self.setLayout(layout)