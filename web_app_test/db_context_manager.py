from mysql import connector


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
        # TODO: необходимо добавить обработку ошибок при установке соединения с БД
        self.conn = connector.connect(**self.configuration)
        self.cr = self.conn.cursor()
        return self.cr

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
