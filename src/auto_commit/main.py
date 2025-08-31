import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto-Commit")
        self.setGeometry(100, 100, 800, 600)
        # TODO: Add repo table, toolbar, etc.

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
