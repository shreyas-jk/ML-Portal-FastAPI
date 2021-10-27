from datetime import datetime

class Logger():
    def write_log(self, file, log_message):
        file.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + log_message + '\n'))
        file.flush()
