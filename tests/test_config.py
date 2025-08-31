import pytest
import json
from unittest.mock import MagicMock

from auto_commit.config import load_config, save_config, RepoEntry, Config, Status

def test_config_creation():
    config = Config()
    assert config.monitored_repos == []

def test_repo_entry_creation():
    repo = RepoEntry(path="/test", has_origin=True)
    assert repo.path == "/test"
    assert repo.has_origin == True
    assert repo.last_status == Status.OK
    assert repo.debounce_ms == 2000
    assert repo.auto_init == False
    assert repo.paused == False

def test_load_config(tmp_path, mocker):
    config_path = tmp_path / "config.json"
    data = {
        "monitored_repos": [{
            "path": "/test",
            "has_origin": True
        }]
    }
    config_path.write_text(json.dumps(data))
    mocker.patch('auto_commit.config.get_config_path', return_value=config_path)
    config = load_config()
    assert len(config.monitored_repos) == 1
    assert config.monitored_repos[0].path == "/test"

def test_save_config(tmp_path, mocker):
    config_path = tmp_path / "config.json"
    mocker.patch('auto_commit.config.get_config_path', return_value=config_path)
    config = Config()
    config.monitored_repos.append(RepoEntry(path="/test", has_origin=True))
    save_config(config)
    assert config_path.exists()
    data = json.loads(config_path.read_text())
    assert len(data["monitored_repos"]) == 1
    assert data["monitored_repos"][0]["path"] == "/test"

def test_load_config_full(tmp_path, mocker):
    config_path = tmp_path / "config.json"
    data = {
        "monitored_repos": [
            {
                "path": "/test",
                "has_origin": True,
                "last_status": "ERROR",
                "debounce_ms": 3000,
                "auto_init": True,
                "paused": True
            }
        ],
        "ui": {
            "window_size": [800, 600],
            "column_widths": [400, 100, 100],
            "minimized_to_tray": True
        },
        "settings": {
            "debounce_ms_default": 2500,
            "gh_token_env": "MY_TOKEN"
        }
    }
    config_path.write_text(json.dumps(data))
    mocker.patch('auto_commit.config.get_config_path', return_value=config_path)
    config = load_config()
    assert len(config.monitored_repos) == 1
    repo = config.monitored_repos[0]
    assert repo.path == "/test"
    assert repo.last_status == Status.ERROR
    assert repo.debounce_ms == 3000
    assert repo.auto_init == True
    assert repo.paused == True
    assert config.ui.window_size == [800, 600]
    assert config.settings.debounce_ms_default == 2500
    assert config.ui.window_size == [800, 600]
