import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from PyQt6.QtWidgets import QApplication

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import WaterReminderApp


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    return app


@pytest.fixture
def reminder(qapp):
    return WaterReminderApp()


def test_window_title(reminder):
    assert reminder.windowTitle() == "Water Reminder"


def test_minutes_input_configuration(reminder):
    assert reminder.minutes_input.minimum() == 1
    assert reminder.minutes_input.maximum() == 1440


def test_message_input_exists(reminder):
    assert reminder.message_input is not None


def test_start_timer(reminder):
    reminder.minutes_input.setValue(10)

    reminder.start_timer()

    assert reminder.timer.isActive()
    assert reminder.timer.interval() == 10 * 60 * 1000

    assert (
        reminder.status_label.text()
        == "Running (10 minute interval)"
    )


def test_stop_timer(reminder):
    reminder.start_timer()

    reminder.stop_timer()

    assert not reminder.timer.isActive()

    assert (
        reminder.status_label.text()
        == "Timer Stopped"
    )


def test_save_settings(
    reminder,
    tmp_path,
    monkeypatch
):
    config_file = tmp_path / "config.json"

    monkeypatch.setattr(
        "app.CONFIG_FILE",
        str(config_file)
    )

    reminder.minutes_input.setValue(15)

    reminder.message_input.setText(
        "Drink Water"
    )

    with patch(
        "app.QMessageBox.information"
    ):
        reminder.save_settings()

    with open(config_file) as f:
        data = json.load(f)

    assert data["minutes"] == 15
    assert data["message"] == "Drink Water"


def test_load_settings(
    reminder,
    tmp_path,
    monkeypatch
):
    config_file = tmp_path / "config.json"

    config_file.write_text(
        json.dumps(
            {
                "minutes": 25,
                "message": "Hydrate"
            }
        )
    )

    monkeypatch.setattr(
        "app.CONFIG_FILE",
        str(config_file)
    )

    reminder.load_settings()

    assert (
        reminder.minutes_input.value()
        == 25
    )

    assert (
        reminder.message_input.text()
        == "Hydrate"
    )


def test_show_reminder_restarts_timer(
    reminder
):
    reminder.minutes_input.setValue(1)

    with patch(
        "app.ReminderPopup"
    ) as popup_mock:
        reminder.show_reminder()

        popup_mock.assert_called_once()

        popup_mock.return_value.exec.assert_called_once()

        assert reminder.timer.isActive()