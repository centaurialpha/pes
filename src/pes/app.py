import logging
import sys
import argparse

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import (
    QFontDatabase,
    QFont,
)

from pes import resources
from pes import __version__
from pes import theme
from pes.main_window import IDE

logger = logging.getLogger("pes")


def get_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )
    return parser


def setup_logger(loglevel):
    FORMAT = "[%(asctime)s] [%(levelname)-6s]: %(name)s:%(funcName)-5s %(message)s"
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    root = logging.getLogger()
    formatter = logging.Formatter(FORMAT, TIME_FORMAT)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root.setLevel(loglevel)
    root.addHandler(handler)


def start():
    args = get_cli().parse_args()
    setup_logger(args.loglevel)
    logger.info("Starting PES %s", __version__)

    app = QApplication(sys.argv)
    app.setApplicationName("pes")

    # Add Font Awesome
    font_family = QFontDatabase.applicationFontFamilies(
        QFontDatabase.addApplicationFont(":font/awesome")
    )[0]
    font = QFont(font_family)
    font.setStyleName("Solid")
    app.setFont(font)

    theme.apply_theme(app)

    ide = IDE()
    ide.show()

    sys.exit(app.exec_())
