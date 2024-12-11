import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from helpers import log
import logging

import rc_resources

#------------------------------------------------------------------------------
def main() -> None:

    log.init_log('default.log', level=logging.INFO)#DEBUG
    logger = logging.getLogger(__name__)
    logger.info("Logger intitialized")

    import backend as bak
    import model
    import state
    
    app = QGuiApplication(sys.argv)
    state.register_for_qml(app)
    engine = QQmlApplicationEngine()
        
    backend = bak.Backend( qml_file="main.qml", app=app, engine=engine, model=model.Model(app, engine=engine) )
    logger.info("App initialized, running")
    retval = backend.run()
    logger.info("App ended, exiting")
    sys.exit(retval)

#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

