import logging
import os

from PyQt5.QtCore import (
    QObject,
    QStandardPaths,
)

BASE_DIR = QStandardPaths.writableLocation(QStandardPaths.ApplicationsLocation)
ROOT_DIR = os.path.join(BASE_DIR, "pes")

logger = logging.getLogger(__name__)


def create_dirs():
    if not os.path.exists(ROOT_DIR):
        logger.debug("Creating root dir=%s", ROOT_DIR)
        os.makedirs(ROOT_DIR, exist_ok=True)


class FS(QObject):

    def get(self):
        pass

    def put(self):
        pass

    def ls(self):
        pass

    def rm(self):
        pass

    def mkdir(self):
        pass

    def rmdir(self):
        pass
