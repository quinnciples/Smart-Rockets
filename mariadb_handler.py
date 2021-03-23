import logging
import time
import mariadb


class MariaDBHandler(logging.Handler):
    """
    Logging handler for SQLite.
    Based on Vinay Sajip's DBHandler class (http://www.red-dove.com/python_logging.html)

    This version sacrifices performance for thread-safety:
    Instead of using a persistent cursor, we open/close connections for each entry.

    AFAIK this is necessary in multi-threaded applications,
    because SQLite doesn't allow access to objects across threads.
    """

    initial_sql = """CREATE TABLE IF NOT EXISTS log(
                        LogID bigint auto_increment primary key,
                        Created text,
                        FileName text,
                        Name text,
                        LogLevel int,
                        LogLevelName text,
                        Message text,
                        Args text,
                        Module text,
                        FuncName text,
                        LineNo int,
                        Exception text,
                        Process int,
                        Thread text,
                        ThreadName text
                   )"""

    insertion_sql = """INSERT INTO log(
                        Created,
                        FileName,
                        Name,
                        LogLevel,
                        LogLevelName,
                        Message,
                        Args,
                        Module,
                        FuncName,
                        LineNo,
                        Exception,
                        Process,
                        Thread,
                        ThreadName
                   )
                   VALUES (
                        '%(asctime)s.%(msecs)03d',
                        '%(filename)s',
                        '%(name)s',
                        %(levelno)d,
                        '%(levelname)s',
                        '%(message)s',
                        '%(args)s',
                        '%(module)s',
                        '%(funcName)s',
                        %(lineno)d,
                        '%(exc_text)s',
                        %(process)d,
                        '%(thread)s',
                        '%(threadName)s'
                   );
                   """

    def __init__(self):

        logging.Handler.__init__(self)
        # Create table if needed:
        self.conn = mariadb.connect(
            user="alexander",
            password="udder1998",
            host="pi.hole",
            port=3306,
            database="logs")
        self.conn.autocommit = False
        self.cursor = self.conn.cursor()
        self.cursor.execute(MariaDBHandler.initial_sql)
        self.conn.commit()
        # self.conn.close()

    def formatDBTime(self, record):
        record.dbtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))

    def emit(self, record):

        # Use default formatting:
        self.format(record)
        # Set the database time up:
        self.formatDBTime(record)
        if record.exc_info:
            record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
        else:
            record.exc_text = ""
        # Insert log record:
        record_dict = {k: self.conn.escape_string(v) if type(v) == str else v for k, v in record.__dict__.items()}
        # record_dict['message'] = self.conn.escape_string(record_dict['message'])
        sql = MariaDBHandler.insertion_sql % record_dict
        self.cursor.execute(sql)
        self.conn.commit()
        # self.conn.close()

    def __del__(self):
        self.conn.close()

    def __exit__(self, type, value, traceback):
        self.conn.close()
