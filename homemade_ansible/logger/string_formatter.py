import logging


class StringFormatter(logging.Formatter):

    def __init__(self, max_length=200):
        fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        super(StringFormatter, self).__init__(fmt)
        self.max_length = max_length

    def format(self, record):
        if len(record.msg) > self.max_length:
            record.msg = record.msg[:self.max_length] + "..."
        return super().format(record)
