import sys

from PySide6.QtGui import QGuiApplication

from helpers import log
import logging

import rc_resources

#------------------------------------------------------------------------------
def main() -> None:

    log.init_log('default.log')
    logger = logging.getLogger(__name__)
    logger.info("Logger intiialized")

    import backend as bak
    import model
    
    app = QGuiApplication(sys.argv)
    backend = bak.Backend( qml_file="main.qml", app=app, model=model.Model(app) )
    logger.info("App initialized, running")
    retval = backend.run()
    logger.info("App ended, exiting")
    sys.exit(retval)

#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

