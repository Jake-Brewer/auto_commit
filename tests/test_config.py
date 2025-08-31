import pytest
from auto_commit.config import Config, RepoEntry, load_config, save_config
from unittest.mock import patch
import json

def test_config_creation():
    config = Config()
    assert config.monitored_repos == []
    assert config.ui.window_size == [960, 640]
    assert config.settings.gh_token_env == "GH_TOKEN"

def test_repo_entry_creation():
    repo = RepoEntry(path="/test", has_origin=True, debounce_ms=3000)
    assert repo.path == "/test"
    assert repo.has_origin == True
    assert repo.debounce_ms == 3000
    assert repo.last_status == "OK"

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
    from auto_commit.config import Status
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
