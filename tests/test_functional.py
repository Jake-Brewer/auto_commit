import pytest

@pytest.mark.functional
@pytest.mark.timeout(60)
def test_functional_add_remove_repo(mocker):
    from auto_commit.main import MainWindow
    mock_config = mocker.patch('auto_commit.main.load_config')
    mock_save = mocker.patch('auto_commit.main.save_config')
    mock_check = mocker.patch('auto_commit.main.check_has_origin', return_value=True)
    mock_dialog = mocker.patch('auto_commit.main.QFileDialog.getExistingDirectory', return_value='/test')
    mock_tray = mocker.patch('auto_commit.main.QSystemTrayIcon')
    window = MainWindow()
    window.add_repo()
    mock_save.assert_called()
    assert len(window.config.monitored_repos) == 1
    # Mock table for remove
    mock_table = mocker.patch.object(window, 'table')
    mock_table.currentRow.return_value = 0
    window.remove_repo()
    mock_save.assert_called()
    assert len(window.config.monitored_repos) == 0
