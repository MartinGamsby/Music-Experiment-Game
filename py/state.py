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
    NONE, INIT, WELCOME, MAIN_MENU, SETTINGS, PLAY_MIDIS, GAME = range(7)
@QmlElement
class StateEnum(QObject):
    QEnum(State)

#------------------------------------------------------------------------------
class MusicState(Enum):
    NONE, INIT, IDLE, PREPARING, GENERATING, PLAYING, ERROR = range(7)
@QmlElement
class MusicStateEnum(QObject):
    QEnum(MusicState)
    
#------------------------------------------------------------------------------
def register_for_qml(app):
    qmlRegisterSingletonInstance(QObject, QML_IMPORT_NAME, QML_IMPORT_MAJOR_VERSION, 0, "App", app)
