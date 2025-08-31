import pytest
from unittest.mock import patch, MagicMock
import sys

sys.modules['PySide6'] = MagicMock()
sys.modules['PySide6.QtWidgets'] = MagicMock()
sys.modules['PySide6.QtGui'] = MagicMock()
sys.modules['PySide6.QtCore'] = MagicMock()

@pytest.mark.e2e
@pytest.mark.timeout(120)
def test_e2e_app_start(mocker):
    mock_app = mocker.patch('PySide6.QtWidgets.QApplication')
    mock_window = mocker.patch('PySide6.QtWidgets.QMainWindow')
    mock_tray = mocker.patch('PySide6.QtWidgets.QSystemTrayIcon')
    mock_icon = mocker.patch('PySide6.QtGui.QIcon')
    mock_action = mocker.patch('PySide6.QtGui.QAction')
    mock_menu = mocker.patch('PySide6.QtWidgets.QMenu')
    mock_app.return_value.exec.return_value = 0
    with patch('sys.exit'):
        from auto_commit.main import main
        main()
    mock_app.assert_called_once()
    mock_tray.assert_called_once()
