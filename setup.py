"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['iTunesAutoSync.py']
DATA_FILES = ['app_icon.png']
OPTIONS = {
    'iconfile':'app_icon.icns',
    'plist': {'LSUIElement': True}
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['watchdog', 'PyQt5']
)