import sys

from PySide6.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu, QTableWidget, QTableWidgetItem, QToolBar, QStatusBar, QFileDialog, QMessageBox, QCheckBox, QAction
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer, QObject

from .config import load_config, save_config, Config, RepoEntry
from .git_agent import check_has_origin

class ConfigController(QObject):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self.save)

    def schedule_save(self):
        self.save_timer.start(300)

    def save(self):
        save_config(self.config)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto-Commit")
        self.setGeometry(100, 100, 800, 600)
        self.config = load_config()
        self.controller = ConfigController(self.config)
        self.init_ui()
        self.populate_table()

    def closeEvent(self, event):
        self.config.ui.window_size = [self.width(), self.height()]
        self.config.ui.column_widths = [self.table.columnWidth(i) for i in range(self.table.columnCount())]
        self.controller.schedule_save()
        event.accept()

    def init_ui(self):
        # Toolbar
        toolbar = self.addToolBar("Main")
        add_action = QAction("Add Folder", self)
        add_action.triggered.connect(self.add_repo)
        toolbar.addAction(add_action)
        remove_action = QAction("Remove Folder", self)
        remove_action.triggered.connect(self.remove_repo)
        toolbar.addAction(remove_action)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Path", "Status", "Debounce (ms)", "Paused"])
        self.setCentralWidget(self.table)

        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")

    def populate_table(self):
        self.table.setRowCount(len(self.config.monitored_repos))
        for row, repo in enumerate(self.config.monitored_repos):
            self.table.setItem(row, 0, QTableWidgetItem(repo.path))
            self.table.setItem(row, 1, QTableWidgetItem(repo.last_status.value))
            self.table.setItem(row, 2, QTableWidgetItem(str(repo.debounce_ms)))
            checkbox = QCheckBox()
            checkbox.setChecked(repo.paused)
            self.table.setCellWidget(row, 3, checkbox)

    def add_repo(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Repository Folder")
        if folder:
            if not check_has_origin(folder):
                reply = QMessageBox.question(self, "Git Init", "Selected folder is not a Git repository. Initialize Git?", QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    # git init
                    import subprocess
                    subprocess.run(["git", "init"], cwd=folder)
                    subprocess.run(["git", "add", "."], cwd=folder)
                    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=folder)
                else:
                    return
            repo = RepoEntry(path=folder, has_origin=check_has_origin(folder))
            self.config.monitored_repos.append(repo)
            self.controller.schedule_save()
            self.populate_table()

    def remove_repo(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            del self.config.monitored_repos[current_row]
            self.controller.schedule_save()
            self.populate_table()

    def pause_all(self):
        for repo in self.config.monitored_repos:
            repo.paused = True
        self.controller.schedule_save()
        self.populate_table()

    def resume_all(self):
        for repo in self.config.monitored_repos:
            repo.paused = False
        self.controller.schedule_save()
        self.populate_table()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # System tray
    tray = QSystemTrayIcon(QIcon(), app)
    tray.setToolTip("Auto-Commit")
    menu = QMenu()
    open_action = QAction("Open Window", app)
    open_action.triggered.connect(window.show)
    pause_action = QAction("Pause All", app)
    pause_action.triggered.connect(lambda: window.pause_all())
    resume_action = QAction("Resume All", app)
    resume_action.triggered.connect(lambda: window.resume_all())
    quit_action = QAction("Quit", app)
    quit_action.triggered.connect(app.quit)
    menu.addAction(open_action)
    menu.addAction(pause_action)
    menu.addAction(resume_action)
    menu.addAction(quit_action)
    tray.setContextMenu(menu)
    tray.show()
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
