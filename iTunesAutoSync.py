from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import csv
import sys
import shutil
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MenuApp(QApplication):

    def __init__(self):
        super(MenuApp, self).__init__([])
        self.setQuitOnLastWindowClosed(False)

        self.icon = QIcon("app_icon.png")

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)

        self.menu = QMenu()

        self.directories_action = QAction("Choose Directories")
        self.directories_action.triggered.connect(self.choose_directories)
        self.menu.addAction(self.directories_action)

        self.start_action = QAction("Start")
        self.start_action.triggered.connect(self.start)
        self.menu.addAction(self.start_action)

        self.stop_action = QAction("Stop")
        self.stop_action.triggered.connect(self.stop)
        self.menu.addAction(self.stop_action)

        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.quit_app)
        self.menu.addAction(self.quit_action)

        self.tray.setContextMenu(self.menu)

    def choose_directories(self):
        downloads_msgbox = QMessageBox()
        downloads_msgbox.setWindowTitle("Select Downloads Folder")
        downloads_msgbox.setText("Select Downloads Folder")
        downloads_msgbox.setStandardButtons(QMessageBox.Ok)
        downloads_msgbox.exec()
        self.downloads_folder = str(QFileDialog.getExistingDirectory(None))

        itunes_msgbox = QMessageBox()
        itunes_msgbox.setWindowTitle("Select iTunes Folder")
        itunes_msgbox.setText("Select iTunes Folder")
        itunes_msgbox.setStandardButtons(QMessageBox.Ok)
        itunes_msgbox.exec()
        self.itunes_folder = str(
            QFileDialog.getExistingDirectory(None)) + "/iTunes Media/Automatically Add to iTunes.localized"

        with open('paths.csv', "w") as f:
            csv_writer = csv.writer(f)

            csv_writer.writerow(["downloads", "itunes"])
            csv_writer.writerow([self.downloads_folder, self.itunes_folder])

    def start(self):
        try:
            observer = Automator()
            observer.start()
        except:
            error_msgbox = QMessageBox()
            error_msgbox.setWindowTitle("Error")
            error_msgbox.setText("Directories have not been chosen.")
            error_msgbox.setStandardButtons(QMessageBox.Ok)
            error_msgbox.exec()
        else:
            start_msgbox = QMessageBox()
            start_msgbox.setWindowTitle("Started")
            start_msgbox.setText("Automator has started")
            start_msgbox.setStandardButtons(QMessageBox.Ok)
            start_msgbox.exec()

    def stop(self):
        observer = Automator()
        observer.stop()

        stop_msgbox = QMessageBox()
        stop_msgbox.setWindowTitle("Stopped")
        stop_msgbox.setText("Automator has stopped")
        stop_msgbox.setStandardButtons(QMessageBox.Ok)
        stop_msgbox.exec()

    def quit_app(self):
        sys.exit()


class MyHandler(FileSystemEventHandler):

    def __init__(self, file_path, autoaddfolder):
        self.file_path = file_path
        self.autoaddfolder = autoaddfolder

    def on_modified(self, event):
        for roots, dirs, files in os.walk(self.file_path):
            for file in files:
                if file.endswith(".mp3") or file.endswith(".wav"):
                    song = self.file_path + "/" + file
                    auto_add_song = self.autoaddfolder + "/" + file
                    shutil.move(song, auto_add_song)

            for dir in dirs:
                folders = os.path.join(roots, dir)
                for x in os.listdir(folders):
                    if x.endswith(".mp3") or x.endswith(".wav"):
                        songs = folders + "/" + x
                        auto_add_folder = self.autoaddfolder + "/" + x
                        shutil.move(songs, auto_add_folder)


class Automator:
    def __init__(self):
        try:
            with open('paths.csv') as f:
                csv_reader = csv.reader(f)

                next(csv_reader)

                for line in csv_reader:
                    self.downloads_folder = line[0]
                    self.itunes_folder = line[1]
        except:
            pass

        try:
            self.event_handler = MyHandler(self.downloads_folder, self.itunes_folder)
            self.observer = Observer()
            self.observer.schedule(self.event_handler, self.downloads_folder, recursive=True)
        except:
            pass

    def start(self):
        self.observer.start()

    def stop(self):
        try:
            self.observer.stop()
        except:
            print("Error")


def run():
    app = MenuApp()
    sys.exit(app.exec_())


run()
