import logging
import helpers.file_helper as fh

#------------------------------------------------------------------------------
def init_log(log_filename, level=logging.INFO):
    #format = '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    #console_format = '%(name)-12s: %(levelname)-8s %(message)s'
    file_format = '[%(asctime)s] %(name)s:%(lineno)d %(levelname)s - %(message)s'
    console_format = '[%(asctime)s] %(name)-20s: %(levelname)-8s %(message)s'
    
    logging.basicConfig(
         filename=fh.get_appdata_file(log_filename, "Logs"),
         level=level, 
         format=file_format,
         datefmt='%H:%M:%S'
     )

    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # set a format which is simpler for console use
    formatter = logging.Formatter(console_format)
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    