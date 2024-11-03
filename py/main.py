import sys

import backend as bak
import model

import rc_resources

#------------------------------------------------------------------------------
def main() -> None:

    backend = bak.Backend( qml_file="main.qml", model=model.Model() )
    sys.exit(backend.run())

#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

