from utils import logger
from batch.workers import Manager


class Main:

    __INIT = False

    def __init__(self):
        if Main.__INIT:
            logger.info(logger_name="BATCH", msg="Batch was already Initialized")
        else:
            Main.__INIT = True
            logger.info(logger_name="BATCH", msg="Iniciando Proceso Batch")
            self.manager = Manager()
            self.manager.start_tasks()

