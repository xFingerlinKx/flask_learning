from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import escape

from .log_request import log_request
from . import constants
from .db_context_manager import UseDatabase, ConnectionDbError, CredentialsDbError, SQLError

from .checker import check_logged_in

# from flask import redirect


app = Flask(__name__)
app.config['db_config'] = constants.db_config
app.secret_key = 'YouWillNeverGuessMySecretKey'


# @app.route('/')
# def redirect_to_entry():
#     """
#     Redirecting to '/entry' location.
#     :return: code=302
#     """
#     return redirect(location='/entry')


def search4vowels(phrase: str) -> set:
    """ Returns the set of vowels found in phrase """
    return set('aeiou').intersection(set(phrase))


def search4letters(phrase: str, letters: str='aeiou') -> set:
    """ Returns the set of letters found in phrase """
    return set(letters).intersection(set(phrase))


@app.route('/search4', methods=['GET', 'POST'])
def do_search():
    """
    Извлечение данных из запроса, поиск, логирование (запись) результов в БД.
    :return: HTML
    """
    # 'request.form' --> ImmutableMultiDict([('phrase', 'qweqwe'), ('letters', 'a')])
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))

    try:
        # запись лога в БД
        log_request(request=request, res=results)
    except Exception as err:
        print(f'***** Logging failed with this error: {err} ******')

    return render_template(
        template_name_or_list='results.html',
        the_title=title,
        the_phrase=phrase,
        the_letters=letters,
        the_results=results,
    )


@app.route('/')
@app.route('/entry')
def entry_page():
    """
    Стартовая страница с формой запроса (HTML).
    :return: HTML
    """
    return render_template(
        template_name_or_list='entry.html',
        the_title='Welcome to search4letters on the web!',
    )


@app.route('/login')
def do_login():
    session['logged_in'] = True
    return 'You are logged in.'


@app.route('/logout')
def do_logout():
    session.pop('logged_in')
    return 'You are logged out.'


@app.route('/viewlog')
@check_logged_in
def view_log_file() -> str:
    """
    Отображение результатов логирования из БД в виде HTML-таблицы.

    :return: {HTML} contents of the logs.
    """
    try:
        with UseDatabase(app.config['db_config']) as cr:
            query = """ SELECT phrase, letters, ip, browser_string, results
                        FROM log;
            """
            cr.execute(query)
            contents = cr.fetchall()

        titles = ('Phrase', 'Letters', 'Remote addr', 'User agent', 'Results')

        return render_template(
            template_name_or_list='log.html',
            the_title='The log file results',
            the_row_titles=titles,
            the_data=contents,
        )

    except ConnectionDbError as err:
        print(f'***** Logging failed with this error: {err} ******')
    except CredentialsDbError as err:
        print(f'***** User-id/Pssword issues. Error: {err} ******')
    except SQLError as err:
        print(f'***** Is your query correct? Error: {err} *****')
    except Exception as err:
        print(f'***** Something went wrong with: {err} ******')
    return 'ERROR'

if __name__ == '__main__':
    app.run(debug=True)
