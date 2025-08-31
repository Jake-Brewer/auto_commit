import pytest
from auto_commit.watcher import AutoCommitHandler, FileWatcher
from unittest.mock import patch, MagicMock

@pytest.mark.timeout(30)
def test_auto_commit_handler_modified(mocker):
    mock_queue = MagicMock()
    handler = AutoCommitHandler('/test', mock_queue)
    mock_event = MagicMock()
    mock_event.is_directory = False
    mock_event.src_path = '/test/file.txt'
    handler.on_modified(mock_event)
    mock_queue.put.assert_called_with(('modified', '/test/file.txt'))

@pytest.mark.timeout(30)
def test_auto_commit_handler_created(mocker):
    mock_queue = MagicMock()
    handler = AutoCommitHandler('/test', mock_queue)
    mock_event = MagicMock()
    mock_event.is_directory = False
    mock_event.src_path = '/test/file.txt'
    handler.on_created(mock_event)
    mock_queue.put.assert_called_with(('created', '/test/file.txt'))

@pytest.mark.timeout(30)
def test_auto_commit_handler_deleted(mocker):
    mock_queue = MagicMock()
    handler = AutoCommitHandler('/test', mock_queue)
    mock_event = MagicMock()
    mock_event.is_directory = False
    mock_event.src_path = '/test/file.txt'
    handler.on_deleted(mock_event)
    mock_queue.put.assert_called_with(('deleted', '/test/file.txt'))

@pytest.mark.timeout(30)
def test_auto_commit_handler_directory(mocker):
    mock_queue = MagicMock()
    handler = AutoCommitHandler('/test', mock_queue)
    mock_event = MagicMock()
    mock_event.is_directory = True
    mock_event.src_path = '/test/dir'
    handler.on_modified(mock_event)
    mock_queue.put.assert_not_called()

@pytest.mark.timeout(30)
def test_file_watcher(mocker):
    mock_queue = MagicMock()
    mock_observer_class = mocker.patch('auto_commit.watcher.Observer')
    mock_observer = MagicMock()
    mock_observer_class.return_value = mock_observer
    watcher = FileWatcher('/test', mock_queue)
    watcher.start()
    mock_observer.schedule.assert_called_once()
    mock_observer.start.assert_called_once()
    watcher.stop()
    mock_observer.stop.assert_called_once()
    mock_observer.join.assert_called_once()
