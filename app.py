import json
import os
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSpinBox,
    QLineEdit,
    QMessageBox
)

from reminder_popup import ReminderPopup


CONFIG_FILE = "config.json"


class WaterReminderApp(QWidget):

    def __init__(self):
        super().__init__()

        self.timer = QTimer()
        self.timer.timeout.connect(
            self.show_reminder
        )

        self.init_ui()

        self.load_settings()

    def init_ui(self):
        self.setWindowTitle(
            "Water Reminder"
        )

        self.resize(400, 250)

        main_layout = QVBoxLayout()


        minutes_label = QLabel(
            "Reminder Interval (Minutes)"
        )

        self.minutes_input = QSpinBox()
        self.minutes_input.setMinimum(1)
        self.minutes_input.setMaximum(1440)


        message_label = QLabel(
            "Reminder Message"
        )

        self.message_input = QLineEdit()


        self.start_button = QPushButton(
            "Start"
        )

        self.stop_button = QPushButton(
            "Stop"
        )

        self.save_button = QPushButton(
            "Save Settings"
        )

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.start_button
        )

        button_layout.addWidget(
            self.stop_button
        )

        button_layout.addWidget(
            self.save_button
        )

        self.status_label = QLabel(
            "Timer Stopped"
        )

        main_layout.addWidget(
            minutes_label
        )

        main_layout.addWidget(
            self.minutes_input
        )

        main_layout.addWidget(
            message_label
        )

        main_layout.addWidget(
            self.message_input
        )

        main_layout.addLayout(
            button_layout
        )

        main_layout.addWidget(
            self.status_label
        )

        self.setLayout(main_layout)


        self.start_button.clicked.connect(
            self.start_timer
        )

        self.stop_button.clicked.connect(
            self.stop_timer
        )

        self.save_button.clicked.connect(
            self.save_settings
        )

    def start_timer(self):
        minutes = self.minutes_input.value()

        milliseconds = (
            minutes * 60 * 1000
        )

        self.timer.start(
            milliseconds
        )

        self.status_label.setText(
            f"Running ({minutes} minute interval)"
        )

    def stop_timer(self):
        self.timer.stop()

        self.status_label.setText(
            "Timer Stopped"
        )

    def show_reminder(self):
        self.timer.stop()

        popup = ReminderPopup(
            self.message_input.text()
        )

        popup.exec()

        self.start_timer()

    def save_settings(self):
        data = {
            "minutes":
                self.minutes_input.value(),
            "message":
                self.message_input.text()
        }

        try:
            with open(
                CONFIG_FILE,
                "w"
            ) as file:
                json.dump(
                    data,
                    file,
                    indent=2
                )

            QMessageBox.information(
                self,
                "Success",
                "Settings saved."
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )

    def load_settings(self):
        if not os.path.exists(
            CONFIG_FILE
        ):
            return

        try:
            with open(
                CONFIG_FILE,
                "r"
            ) as file:
                data = json.load(
                    file
                )

            self.minutes_input.setValue(
                data.get(
                    "minutes",
                    30
                )
            )

            self.message_input.setText(
                data.get(
                    "message",
                    "Drink Water"
                )
            )

        except Exception:
            pass


def main():
    app = QApplication(
        sys.argv
    )

    window = WaterReminderApp()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()