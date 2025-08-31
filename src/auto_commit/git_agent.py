from git import Repo, GitCommandError
from pathlib import Path

def check_has_origin(repo_path: str) -> bool:
    try:
        repo = Repo(repo_path)
        repo.remote('origin')
        return True
    except:
        return False

def commit_repo(repo_path: str, message: str, has_origin: bool) -> str:
    try:
        repo = Repo(repo_path)
        repo.git.add('-A')
        repo.index.commit(message)
        if has_origin:
            origin = repo.remote('origin')
            origin.push()
        return "OK"
    except GitCommandError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"
