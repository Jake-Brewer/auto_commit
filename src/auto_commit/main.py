import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QTableWidget, QTableWidgetItem, QToolBar, QStatusBar, QFileDialog, QMessageBox, QCheckBox
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QTimer

from .config import load_config, save_config, Config, RepoEntry
from .git_agent import check_has_origin

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto-Commit")
        self.setGeometry(100, 100, 800, 600)
        self.config = load_config()
        self.init_ui()
        self.populate_table()

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
            self.table.setItem(row, 1, QTableWidgetItem(repo.last_status))
            self.table.setItem(row, 2, QTableWidgetItem(str(repo.debounce_ms)))
            checkbox = QCheckBox()
            checkbox.setChecked(repo.paused)
            self.table.setCellWidget(row, 3, checkbox)

    def add_repo(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Repository Folder")
        if folder:
            if not check_has_origin(folder):
                QMessageBox.warning(self, "Warning", "Selected folder is not a Git repository.")
                return
            repo = RepoEntry(path=folder, has_origin=check_has_origin(folder))
            self.config.monitored_repos.append(repo)
            save_config(self.config)
            self.populate_table()

    def remove_repo(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            del self.config.monitored_repos[current_row]
            save_config(self.config)
            self.populate_table()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # System tray
    tray = QSystemTrayIcon(QIcon(), app)
    tray.setToolTip("Auto-Commit")
    menu = QMenu()
    open_action = QAction("Open", app)
    open_action.triggered.connect(window.show)
    quit_action = QAction("Quit", app)
    quit_action.triggered.connect(app.quit)
    menu.addAction(open_action)
    menu.addAction(quit_action)
    tray.setContextMenu(menu)
    tray.show()
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
