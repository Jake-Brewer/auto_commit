import pytest
from auto_commit.git_agent import check_has_origin, commit_repo
from unittest.mock import patch, MagicMock

@pytest.mark.timeout(30)
def test_check_has_origin_true(mocker):
    mock_repo_class = mocker.patch('auto_commit.git_agent.Repo')
    mock_repo = MagicMock()
    mock_repo_class.return_value = mock_repo
    mock_repo.remote.return_value = MagicMock()
    assert check_has_origin('/test') == True

@pytest.mark.timeout(30)
def test_check_has_origin_false(mocker):
    mock_repo_class = mocker.patch('auto_commit.git_agent.Repo', side_effect=Exception)
    assert check_has_origin('/test') == False

@pytest.mark.timeout(60)
@pytest.mark.slow
def test_commit_repo_success(mocker):
    mock_repo_class = mocker.patch('auto_commit.git_agent.Repo')
    mock_repo = MagicMock()
    mock_repo_class.return_value = mock_repo
    mock_remote = MagicMock()
    mock_repo.remote.return_value = mock_remote
    result = commit_repo('/test', 'auto-commit 2025-08-31 01:00:00', True)
    assert result == "OK"
    mock_repo.git.add.assert_called_with('-A')
    mock_repo.index.commit.assert_called_with('auto-commit 2025-08-31 01:00:00')
    mock_remote.push.assert_called_once()

@pytest.mark.timeout(30)
def test_commit_repo_error(mocker):
    mock_repo_class = mocker.patch('auto_commit.git_agent.Repo')
    mock_repo = MagicMock()
    mock_repo_class.return_value = mock_repo
    mock_repo.git.add.side_effect = Exception("add failed")
    result = commit_repo('/test', 'message', False)
    assert "add failed" in result
