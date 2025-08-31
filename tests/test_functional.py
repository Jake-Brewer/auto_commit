import pytest
import sys
from unittest.mock import MagicMock

sys.modules['PySide6'] = MagicMock()
sys.modules['PySide6.QtWidgets'] = MagicMock()
sys.modules['PySide6.QtGui'] = MagicMock()
sys.modules['PySide6.QtCore'] = MagicMock()

@pytest.mark.functional
@pytest.mark.timeout(60)
def test_functional_add_remove_repo(mocker):
    mock_app = mocker.patch('PySide6.QtWidgets.QApplication')
    mock_window = mocker.patch('PySide6.QtWidgets.QMainWindow')
    mock_tray = mocker.patch('PySide6.QtWidgets.QSystemTrayIcon')
    mock_icon = mocker.patch('PySide6.QtGui.QIcon')
    mock_action = mocker.patch('PySide6.QtGui.QAction')
    mock_menu = mocker.patch('PySide6.QtWidgets.QMenu')
    mock_table = mocker.patch('PySide6.QtWidgets.QTableWidget')
    mock_item = mocker.patch('PySide6.QtWidgets.QTableWidgetItem')
    mock_checkbox = mocker.patch('PySide6.QtWidgets.QCheckBox')
    mock_dialog = mocker.patch('PySide6.QtWidgets.QFileDialog.getExistingDirectory', return_value='/test')
    mock_message = mocker.patch('PySide6.QtWidgets.QMessageBox.warning')
    mock_config = mocker.patch('auto_commit.main.load_config', return_value=type('Config', (), {'monitored_repos': []})())
    mock_save = mocker.patch('auto_commit.main.save_config')
    mock_check = mocker.patch('auto_commit.main.check_has_origin', return_value=True)
    from auto_commit.main import MainWindow
    window = MainWindow()
    window.add_repo()
    mock_save.assert_called()
    assert len(window.config.monitored_repos) == 1
    # Mock table for remove
    mock_table_instance = mock_table.return_value
    mock_table_instance.currentRow.return_value = 0
    window.remove_repo()
    mock_save.assert_called()
    assert len(window.config.monitored_repos) == 0
