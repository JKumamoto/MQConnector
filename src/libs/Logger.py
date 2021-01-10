import logging

class Logger():

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        e_handler = logging.FileHandler('erros.log')
        f_handler = logging.FileHandler('app.log')
        event_handler = logging.FileHandler('events.log')

        e_handler.setLevel(logging.ERROR)

        log_format = logging.Formatter('[%(asctime)s] - %(levelname)s - %(name)s - %(message)s')
        f_handler.setFormatter(log_format)
        e_handler.setFormatter(log_format)

        self.logger.addHandler(f_handler)
        self.logger.addHandler(e_handler)

    def debug(self, message):
        self.logger.debug(message)
        return self

    def info(self, message):
        self.logger.info(message);
        return self

    def warning(self, message):
        self.logger.info(message);
        return self

    def error(self, message):
        self.logger.info(message);
        return self

