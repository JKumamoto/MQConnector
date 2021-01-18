from datetime import datetime

class Logger():

    def __init__(self):
        self.log("INFO", __name__, "Log inicializada")

    def log(self, level, function, message):
        now = datetime.now()
        print(f'{now.strftime("[%d/%m/%Y %H:%M:%S]")} - {level} - {function} - {message}')
        return self

    def post(self, level, function, message):
        jsondata = ""
        return self
