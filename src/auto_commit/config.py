import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List
import platformdirs

@dataclass
class RepoEntry:
    path: str
    has_origin: bool = False
    last_status: str = "OK"
    debounce_ms: int = 2000
    auto_init: bool = False
    paused: bool = False

@dataclass
class UISettings:
    window_size: List[int] = field(default_factory=lambda: [960, 640])
    column_widths: List[int] = field(default_factory=lambda: [420, 120, 120])
    minimized_to_tray: bool = True

@dataclass
class AppSettings:
    debounce_ms_default: int = 2000
    gh_token_env: str = "GH_TOKEN"

@dataclass
class Config:
    monitored_repos: List[RepoEntry] = field(default_factory=list)
    ui: UISettings = field(default_factory=UISettings)
    settings: AppSettings = field(default_factory=AppSettings)

def get_config_path() -> Path:
    config_dir = Path(platformdirs.user_config_dir("auto-commit"))
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"

def load_config() -> Config:
    config_path = get_config_path()
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        config = Config()
        config.monitored_repos = [RepoEntry(**repo) for repo in data.get("monitored_repos", [])]
        config.ui = UISettings(**data.get("ui", {}))
        config.settings = AppSettings(**data.get("settings", {}))
        return config
    return Config()

def save_config(config: Config) -> None:
    config_path = get_config_path()
    data = {
        "monitored_repos": [vars(repo) for repo in config.monitored_repos],
        "ui": vars(config.ui),
        "settings": vars(config.settings)
    }
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
