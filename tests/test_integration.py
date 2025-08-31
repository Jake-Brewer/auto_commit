import pytest
from unittest.mock import MagicMock

@pytest.mark.integration
@pytest.mark.timeout(60)
def test_integration_config_git_flow(mocker, tmp_path):
    from auto_commit.config import load_config, save_config, RepoEntry
    from auto_commit.git_agent import check_has_origin

    # Mock config path
    config_path = tmp_path / "config.json"
    mocker.patch('auto_commit.config.get_config_path', return_value=config_path)

    # Load empty config
    config = load_config()
    # Add repo
    config.monitored_repos.append(RepoEntry(path='/test', has_origin=True))
    save_config(config)

    # Reload
    config2 = load_config()
    assert len(config2.monitored_repos) == 1

    # Mock git
    mock_repo_class = mocker.patch('auto_commit.git_agent.Repo')
    mock_repo = MagicMock()
    mock_repo_class.return_value = mock_repo
    mock_repo.remote.return_value = MagicMock()
    assert check_has_origin('/test') == True
