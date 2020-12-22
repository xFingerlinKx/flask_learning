from mysql import connector
from mysql.connector import errors


class ConnectionDbError(Exception):
    pass


class CredentialsDbError(Exception):
    pass


class SQLError(Exception):
    pass

class UseDatabase:
    """
    Класс диспетчера контекста для контекстного
    менеджера (инструкции with) --> подключение к БД.
    """

    def __init__(self, config):
        """
        Инициализация подключения к БД.
        Для подключения в качестве параметров используется словарь с данными.

        :param config: {dict} словарь с параметрами подключения
        :return: None
        """
        self.configuration = config

    def __enter__(self):
        """
        Метод выполняет настройку объекта перед началом выполнения инструкции with.
        Подключение к БД и возвращение курсора БД.

        :return: {obj} объект курсора для подключения к БД
        """
        try:
            self.conn = connector.connect(**self.configuration)
            self.cr = self.conn.cursor()
            return self.cr
        except errors.InterfaceError as err:
            raise ConnectionDbError(str(err))
        except errors.ProgrammingError as err:
            raise CredentialsDbError(str(err))
        except errors.DataError as err:
            raise SQLError(str(err))

    def __exit__(self, exc_type, exc_value, exc_trace):
        """
        Метод выполняется по завершении тела инструкции with.
        Подтвержение изменений (запись) в БД (commit), закрытие соединения с курсором БД и к самой БД.
        Также служит для обработки исключений, которые возникают внутри блока with.

        :return: None
        """
        self.conn.commit()
        self.cr.close()
        self.conn.close()

        # обработка непредвиденных исключений, которые возникнут в случае, если не завершится блок __enter__
        # если блок __enter__ не завершится в __exit__ передается кортеж значений (exc_type, exc_value, exc_trace)
        # если блок __enter__ завершится в __exit__ передается None в кортеж (exc_type, exc_value, exc_trace)
        if exc_type is errors.ProgrammingError:
            raise SQLError(exc_type)
        elif exc_type:
            raise exc_type(str(exc_value))
