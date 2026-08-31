import os
import sys
import threading
import time

import webview
from waitress import serve


def get_base_dir():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS

    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = get_base_dir()

sys.path.insert(0, BASE_DIR)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "smartpos.settings"
)

import django

django.setup()

from smartpos.wsgi import application


def start_django():
    serve(
        application,
        host="127.0.0.1",
        port=8000,
        threads=8,
    )


def main():

    server_thread = threading.Thread(
        target=start_django,
        daemon=True,
    )

    server_thread.start()

    # Give the local server a moment to start
    time.sleep(2)

    webview.create_window(
        title="SmartPOS",
        url="http://127.0.0.1:8000/",
        width=1440,
        height=900,
        resizable=True,
        maximized=True,
    )

    webview.start()


if __name__ == "__main__":
    main()