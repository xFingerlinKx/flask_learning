from .db_context_manager import UseDatabase
from . import constants


def log_request(request, res: str) -> None:
    """
    Запись результатов запроса в таблицу 'log' БД 'vsearch_log'.

    :param request: {obj} объект запроса
    :param res: {str} результат запроса
    :return: None
    """
    with UseDatabase(constants.db_config) as cr:
        query = """ INSERT INTO log (phrase, letters, ip, browser_string, results)
                    VALUES (%s, %s, %s, %s, %s);
            """
        cr.execute(
            query, (
                request.form['phrase'],
                request.form['letters'],
                request.remote_addr,
                request.user_agent.browser,
                res,
            )
        )
