# From https://stackoverflow.com/questions/67057987/use-qenum-like-a-python-enum
import sys
from enum import Enum
from pathlib import Path

from PySide6.QtCore import Property, QEnum, QObject
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import (
    QmlElement,
    QQmlApplicationEngine,
    qmlRegisterSingletonInstance,
)

#------------------------------------------------------------------------------
QML_IMPORT_NAME = "com.martingamsby.music"
QML_IMPORT_MAJOR_VERSION = 1

#------------------------------------------------------------------------------
class State(Enum):
    INIT, WELCOME = range(2)

#------------------------------------------------------------------------------
@QmlElement
class Enums(QObject):
    QEnum(State)

#------------------------------------------------------------------------------
def register_for_qml(app):
    qmlRegisterSingletonInstance(QObject, "com.example.app", 1, 0, "App", app)
