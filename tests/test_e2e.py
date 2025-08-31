import pytest
from unittest.mock import patch

@pytest.mark.e2e
@pytest.mark.timeout(120)
def test_e2e_app_start(mocker):
    from auto_commit.main import main
    mock_app = mocker.patch('auto_commit.main.QApplication')
    mock_window = mocker.patch('auto_commit.main.MainWindow')
    mock_app.return_value.exec.return_value = 0
    with patch('sys.exit'):
        main()
    mock_app.assert_called_once()
    mock_window.assert_called_once()
