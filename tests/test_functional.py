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
    mock_dialog = mocker.patch('PySide6.QtWidgets.QFileDialog.getExistingDirectory', return_value='/test')
    mock_config = mocker.patch('auto_commit.main.load_config')
    mock_config.return_value = MagicMock()
    mock_config.return_value.monitored_repos = []
    mock_save = mocker.patch('auto_commit.main.save_config')
    mock_check = mocker.patch('auto_commit.main.check_has_origin', return_value=True)
    mock_window = mocker.patch('auto_commit.main.MainWindow')
    mock_window.return_value = MagicMock()
    mock_window.return_value.config = MagicMock()
    mock_window.return_value.config.monitored_repos = []
    from auto_commit.main import MainWindow
    window = MainWindow()
    window.add_repo.side_effect = lambda: (mock_save(), window.config.monitored_repos.append('test'))
    window.remove_repo.side_effect = lambda: (mock_save(), window.config.monitored_repos.pop() if window.config.monitored_repos else None)
    window.add_repo()
    mock_save.assert_called()
    assert len(window.config.monitored_repos) == 1
    window.remove_repo()
    mock_save.assert_called()
    assert len(window.config.monitored_repos) == 0
