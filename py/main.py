import sys

from PySide6.QtGui import QGuiApplication

import backend as bak
import model

import rc_resources

#------------------------------------------------------------------------------
def main() -> None:
    
    app = QGuiApplication(sys.argv)
    backend = bak.Backend( qml_file="main.qml", app=app, model=model.Model(app) )
    sys.exit(backend.run())

#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

