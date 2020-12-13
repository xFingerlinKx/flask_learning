from mysql import connector


dbconfig = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '*******',
    'database': 'vsearch_log'
}


def log_request(request, res: str) -> None:
    """
    Write request and the results in 'log' table 'vsearch_log' db.

    :param request: request obj
    :param res: result of request
    :return: None
    """
    conn = connector.connect(**dbconfig)
    cr = conn.cursor()
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
    conn.commit()
    cr.close()
    conn.close()
